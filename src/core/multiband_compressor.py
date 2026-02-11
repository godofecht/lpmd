# Multi-band compressor using FFT
# Splits audio into frequency bands and compresses each one separately

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple


class MultiBandCompressor(nn.Module):
    # FFT-based multi-band compressor
    # Each frequency bin gets its own compression settings

    def __init__(self,
                 sample_rate=44100,
                 fft_size=4096,
                 hop_size=1024,
                 threshold_db=-20.0,
                 ratio=4.0,
                 attack_ms=10.0,
                 release_ms=100.0,
                 makeup_gain_db=0.0,
                 knee_width_db=0.0):
        # sample_rate: audio sample rate
        # fft_size: must be 4096
        # hop_size: step size for overlap-add
        # threshold_db, ratio, etc: default compression settings
        super(MultiBandCompressor, self).__init__()

        # gotta be 4096
        assert fft_size == 4096

        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.hop_size = hop_size
        self.num_bands = fft_size // 2 + 1  # 2049 bins from real FFT

        # hann window for overlap-add
        self.register_buffer('window', torch.hann_window(fft_size))

        # compression params per band
        self.threshold_db = nn.Parameter(torch.full((self.num_bands,), threshold_db))
        self.ratio = nn.Parameter(torch.full((self.num_bands,), ratio))
        self.makeup_gain_db = nn.Parameter(torch.full((self.num_bands,), makeup_gain_db))
        self.knee_width_db = nn.Parameter(torch.full((self.num_bands,), knee_width_db))

        # convert attack/release to coeffs
        attack_samples = int(attack_ms * sample_rate / 1000)
        release_samples = int(release_ms * sample_rate / 1000)

        self.attack_coeff = 1.0 - torch.exp(torch.tensor(-1.0 / attack_samples)) if attack_samples > 0 else 1.0
        self.release_coeff = 1.0 - torch.exp(torch.tensor(-1.0 / release_samples)) if release_samples > 0 else 1.0

        # envelope state - init later when we know batch size
        self.envelope = None

        # freq bins for reference
        self.register_buffer('freq_bins', torch.fft.rfftfreq(fft_size, 1.0/sample_rate))

    def _db_to_linear(self, db):
        # dB to linear
        return torch.pow(10.0, db / 20.0)

    def _linear_to_db(self, linear):
        # linear to dB
        return 20.0 * torch.log10(torch.clamp(linear, min=1e-8))

    def _compute_gain_reduction(self, input_level_db, threshold_db, ratio, knee_width_db):
        # figure out how much to reduce gain for each band

        # soft knee setup
        knee_start = threshold_db - knee_width_db / 2
        knee_end = threshold_db + knee_width_db / 2

        over_threshold = input_level_db - threshold_db
        knee_region = (input_level_db >= knee_start) & (input_level_db <= knee_end)

        # hard knee compression
        gain_reduction_hard = torch.where(
            input_level_db < threshold_db,
            torch.zeros_like(input_level_db),
            over_threshold * (1.0 - 1.0/ratio)
        )

        # soft knee if enabled
        if knee_width_db.mean() > 0:
            knee_factor = (input_level_db - knee_start) / knee_width_db
            knee_factor = torch.clamp(knee_factor, 0.0, 1.0)

            # quadratic curve for smooth transition
            knee_gain = knee_factor * knee_factor * over_threshold * (1.0 - 1.0/ratio)
            gain_reduction_soft = torch.where(knee_region, knee_gain, gain_reduction_hard)
        else:
            gain_reduction_soft = gain_reduction_hard

        return gain_reduction_soft

    def _apply_attack_release(self, gain_reduction_db, envelope):
        # smooth the gain reduction with attack/release

        target_gain_linear = self._db_to_linear(-gain_reduction_db)

        # pick attack or release coeff based on direction
        coeff = torch.where(target_gain_linear < envelope,
                           self.attack_coeff, self.release_coeff)

        # update envelope state
        new_envelope = envelope + coeff * (target_gain_linear - envelope)
        self.envelope.copy_(new_envelope)

        smoothed_gain_reduction_db = -self._linear_to_db(new_envelope)

        return smoothed_gain_reduction_db

    def forward(self, audio):
        # run compression on audio

        batch_size, num_channels, time_length = audio.shape

        # pad to make divisible by hop size
        pad_length = (self.hop_size - (time_length % self.hop_size)) % self.hop_size
        if pad_length > 0:
            audio = F.pad(audio, (0, pad_length))

        padded_length = audio.shape[-1]
        output = torch.zeros_like(audio)

        # init envelope if needed
        if self.envelope is None or self.envelope.shape[0] != batch_size or self.envelope.shape[1] != num_channels:
            self.envelope = torch.zeros(batch_size, num_channels, self.num_bands, device=audio.device)

        # process in overlapping chunks
        for start in range(0, padded_length - self.fft_size + 1, self.hop_size):
            end = start + self.fft_size

            # window and FFT
            window_audio = audio[:, :, start:end] * self.window.unsqueeze(0).unsqueeze(0)
            fft = torch.fft.rfft(window_audio, dim=-1)

            # get magnitude in dB
            magnitude = torch.abs(fft)
            magnitude_db = self._linear_to_db(magnitude)

            # compress each band
            gain_reduction_db = self._compute_gain_reduction(
                magnitude_db,
                self.threshold_db.unsqueeze(0).unsqueeze(0),
                self.ratio.unsqueeze(0).unsqueeze(0),
                self.knee_width_db.unsqueeze(0).unsqueeze(0)
            )

            # smooth with attack/release
            smoothed_gain_reduction_db = self._apply_attack_release(
                gain_reduction_db,
                self.envelope
            )

            # apply compression + makeup gain
            compressed_magnitude_db = magnitude_db - smoothed_gain_reduction_db + \
                                    self.makeup_gain_db.unsqueeze(0).unsqueeze(0)

            # back to linear
            compressed_magnitude = self._db_to_linear(compressed_magnitude_db)

            # reconstruct with original phase
            phase = torch.angle(fft)
            compressed_fft = compressed_magnitude * torch.exp(1j * phase)
            compressed_audio = torch.fft.irfft(compressed_fft, dim=-1)

            # overlap-add
            output[:, :, start:end] += compressed_audio * self.window.unsqueeze(0).unsqueeze(0)

        # remove padding
        if pad_length > 0:
            output = output[:, :, :-pad_length]

        return output

    def process_with_intermediates(self, audio):
        # return FFT bands, gain curve, and reconstructed audio
        # useful for visualizing compression process

        batch_size, num_channels, time_length = audio.shape

        # pad to make divisible by hop size
        pad_length = (self.hop_size - (time_length % self.hop_size)) % self.hop_size
        if pad_length > 0:
            audio = F.pad(audio, (0, pad_length))

        padded_length = audio.shape[-1]
        output = torch.zeros_like(audio)

        # init envelope if needed
        if self.envelope is None or self.envelope.shape[0] != batch_size or self.envelope.shape[1] != num_channels:
            self.envelope = torch.zeros(batch_size, num_channels, self.num_bands, device=audio.device)

        # collect intermediates for first chunk only (for simplicity)
        fft_bands = None
        gain_curve_db = None
        compressed_fft = None

        # process in overlapping chunks
        for start in range(0, padded_length - self.fft_size + 1, self.hop_size):
            end = start + self.fft_size

            # window and FFT
            window_audio = audio[:, :, start:end] * self.window.unsqueeze(0).unsqueeze(0)
            fft = torch.fft.rfft(window_audio, dim=-1)

            # get magnitude in dB
            magnitude = torch.abs(fft)
            magnitude_db = self._linear_to_db(magnitude)

            # compress each band
            gain_reduction_db = self._compute_gain_reduction(
                magnitude_db,
                self.threshold_db.unsqueeze(0).unsqueeze(0),
                self.ratio.unsqueeze(0).unsqueeze(0),
                self.knee_width_db.unsqueeze(0).unsqueeze(0)
            )

            # smooth with attack/release
            smoothed_gain_reduction_db = self._apply_attack_release(
                gain_reduction_db,
                self.envelope
            )

            # apply compression + makeup gain
            compressed_magnitude_db = magnitude_db - smoothed_gain_reduction_db + \
                                    self.makeup_gain_db.unsqueeze(0).unsqueeze(0)

            # back to linear
            compressed_magnitude = self._db_to_linear(compressed_magnitude_db)

            # reconstruct with original phase
            phase = torch.angle(fft)
            compressed_fft_chunk = compressed_magnitude * torch.exp(1j * phase)
            compressed_audio = torch.fft.irfft(compressed_fft_chunk, dim=-1)

            # overlap-add
            output[:, :, start:end] += compressed_audio * self.window.unsqueeze(0).unsqueeze(0)

            # save intermediates from first chunk
            if fft_bands is None:
                fft_bands = magnitude[0, 0].cpu()  # first channel of first batch
                gain_curve_db = smoothed_gain_reduction_db[0, 0].cpu()
                compressed_fft = compressed_fft_chunk[0, 0].cpu()

        # remove padding
        if pad_length > 0:
            output = output[:, :, :-pad_length]

        return {
            'fft_bands': fft_bands,      # magnitude spectrum (linear)
            'gain_curve_db': gain_curve_db,  # gain reduction in dB
            'compressed_fft': compressed_fft,  # compressed complex FFT
            'reconstructed_audio': output  # final time-domain audio
        }

    def set_band_parameters(self, band_idx, threshold_db=None, ratio=None, makeup_gain_db=None, knee_width_db=None):
        # change compression settings for one band
        if threshold_db is not None:
            self.threshold_db.data[band_idx] = threshold_db
        if ratio is not None:
            self.ratio.data[band_idx] = ratio
        if makeup_gain_db is not None:
            self.makeup_gain_db.data[band_idx] = makeup_gain_db
        if knee_width_db is not None:
            self.knee_width_db.data[band_idx] = knee_width_db

    def get_frequency_range(self, band_idx):
        # get freq range for a band index
        if band_idx == 0:
            low_freq = 0.0
        else:
            low_freq = self.freq_bins[band_idx - 1].item()

        if band_idx >= len(self.freq_bins) - 1:
            high_freq = self.sample_rate / 2
        else:
            high_freq = self.freq_bins[band_idx + 1].item()

        return low_freq, high_freq


def create_example_usage():
    # quick demo
    import numpy as np

    compressor = MultiBandCompressor(
        sample_rate=44100,
        threshold_db=-18.0,
        ratio=3.0,
        attack_ms=5.0,
        release_ms=50.0,
        makeup_gain_db=3.0
    )

    # different settings per freq range
    for i in range(compressor.num_bands):
        low_freq, high_freq = compressor.get_frequency_range(i)
        if low_freq < 200:
            compressor.set_band_parameters(i, threshold_db=-15.0, ratio=2.0)  # gentle low end
        elif low_freq < 2000:
            compressor.set_band_parameters(i, threshold_db=-20.0, ratio=4.0)  # normal mids
        else:
            compressor.set_band_parameters(i, threshold_db=-25.0, ratio=6.0)  # squash highs

    # test signal - freq sweep
    sample_rate = 44100
    duration = 2.0
    t = torch.linspace(0, duration, int(sample_rate * duration))

    freq_sweep = torch.exp(torch.linspace(torch.log(torch.tensor(20.0)),
                                        torch.log(torch.tensor(20000.0)),
                                        len(t)))
    audio = torch.sin(2 * torch.pi * torch.cumsum(freq_sweep / sample_rate, dim=0))

    audio = audio / torch.max(torch.abs(audio))
    audio = audio.unsqueeze(0).unsqueeze(0)

    print(f"Input audio shape: {audio.shape}")

    with torch.no_grad():
        compressed_audio = compressor(audio)

    print(f"Compressed audio shape: {compressed_audio.shape}")
    print("Done!")

    return compressor, audio, compressed_audio


if __name__ == "__main__":
    create_example_usage()
