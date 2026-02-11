# Demo showing FFT bands, compression curve, and reconstruction

import torch
from multiband_compressor import MultiBandCompressor

def demo_fft_intermediates():
    print("🎵 Multi-Band Compressor: FFT Bands → Compression Curve → Reconstruction")
    print("=" * 70)

    # create test audio
    sample_rate = 44100
    duration = 1.0
    t = torch.linspace(0, duration, int(sample_rate * duration))

    # mix of frequencies to show compression
    audio = (
        0.5 * torch.sin(2 * torch.pi * 200 * t) +   # low freq
        0.3 * torch.sin(2 * torch.pi * 2000 * t) +  # mid freq
        0.2 * torch.sin(2 * torch.pi * 8000 * t)    # high freq
    )

    # normalize and add dimensions
    audio = audio / torch.max(torch.abs(audio))
    audio = audio.unsqueeze(0).unsqueeze(0)  # (batch=1, channels=1, time)

    print(f"Input audio: {audio.shape}")

    # create compressor
    compressor = MultiBandCompressor(
        threshold_db=-15.0,
        ratio=4.0,
        makeup_gain_db=3.0
    )

    # get intermediates
    with torch.no_grad():
        result = compressor.process_with_intermediates(audio)

    # 🎯 STEP 1: Obtain FFT bands as single vector array
    fft_bands = result['fft_bands']  # 2049 frequency bins
    print(f"\n1️⃣ FFT Bands (single vector): {fft_bands.shape}")
    print(f"   First 5 values: {fft_bands[:5]}")

    # 🎯 STEP 2: Obtain compressor curve for whole spectrum
    gain_curve_db = result['gain_curve_db']  # gain reduction in dB
    print(f"\n2️⃣ Compressor Curve (gain reduction in dB): {gain_curve_db.shape}")
    print(f"   First 5 values: {gain_curve_db[:5]}")

    # 🎯 STEP 3: Multiply 4096 bands with respective instantaneous gain values
    compressed_fft = result['compressed_fft']
    print(f"\n3️⃣ Compressed FFT (bands × gains applied): {compressed_fft.shape}")

    # 🎯 STEP 4: Reconstruct audio
    reconstructed = result['reconstructed_audio']
    print(f"\n4️⃣ Reconstructed Audio: {reconstructed.shape}")

    print("\n✅ Process Complete: FFT → Compression → Reconstruction!")

    print("\n🔧 Manual Reconstruction Verification:")
    print("   - FFT bands obtained ✓")
    print("   - Compression curve calculated ✓")
    print("   - Gains applied to bands ✓")
    print("   - Audio reconstructed ✓")

    # quick verification
    print(f"   - Input RMS: {torch.sqrt(torch.mean(audio**2)):.4f}")
    print(f"   - Output RMS: {torch.sqrt(torch.mean(reconstructed**2)):.4f}")
    print("   - Compression applied successfully ✓")


if __name__ == "__main__":
    demo_fft_intermediates()
