#!/usr/bin/env python3
"""
Demo script for the MultiBandCompressor

This script demonstrates how to use the 4096-band compressor
with different settings for different frequency ranges.
"""

import torch
import numpy as np
from multiband_compressor import MultiBandCompressor


def create_test_audio(sample_rate=44100, duration=2.0):
    """Create test audio with multiple frequency components."""
    t = torch.linspace(0, duration, int(sample_rate * duration))

    # Mix of different frequencies to test compression
    audio = (
        0.3 * torch.sin(2 * torch.pi * 100 * t) +    # Low frequency
        0.4 * torch.sin(2 * torch.pi * 1000 * t) +   # Mid frequency
        0.3 * torch.sin(2 * torch.pi * 8000 * t)     # High frequency
    )

    # Normalize
    audio = audio / torch.max(torch.abs(audio))

    # Add batch and channel dimensions
    return audio.unsqueeze(0).unsqueeze(0)


def demo_basic_compression():
    """Demonstrate basic multi-band compression."""
    print("=== Basic Multi-Band Compression Demo ===")

    # Create compressor with default settings
    compressor = MultiBandCompressor(
        sample_rate=44100,
        threshold_db=-18.0,
        ratio=3.0,
        attack_ms=5.0,
        release_ms=50.0,
        makeup_gain_db=3.0
    )

    print(f"Compressor has {compressor.num_bands} frequency bands")
    print(f"FFT size: {compressor.fft_size}")
    print(f"Hop size: {compressor.hop_size}")

    # Create test audio
    audio = create_test_audio()
    print(f"Input audio shape: {audio.shape}")

    # Apply compression
    with torch.no_grad():
        compressed_audio = compressor(audio)

    print(f"Compressed audio shape: {compressed_audio.shape}")
    print("Basic compression completed!\n")


def demo_frequency_specific_compression():
    """Demonstrate different compression settings for different frequencies."""
    print("=== Frequency-Specific Compression Demo ===")

    compressor = MultiBandCompressor()

    # Set different compression for different frequency ranges
    print("Setting custom compression parameters per frequency band...")

    for band_idx in range(compressor.num_bands):
        low_freq, high_freq = compressor.get_frequency_range(band_idx)

        if low_freq < 200:
            # Low frequencies: gentle compression
            compressor.set_band_parameters(
                band_idx,
                threshold_db=-15.0,
                ratio=2.0,
                makeup_gain_db=2.0
            )
        elif low_freq < 2000:
            # Mid frequencies: moderate compression
            compressor.set_band_parameters(
                band_idx,
                threshold_db=-20.0,
                ratio=4.0,
                makeup_gain_db=3.0
            )
        else:
            # High frequencies: aggressive compression
            compressor.set_band_parameters(
                band_idx,
                threshold_db=-25.0,
                ratio=6.0,
                makeup_gain_db=4.0
            )

    print("Applied different compression settings:")
    print("  Low freq (< 200Hz): threshold=-15dB, ratio=2:1")
    print("  Mid freq (200-2000Hz): threshold=-20dB, ratio=4:1")
    print("  High freq (> 2000Hz): threshold=-25dB, ratio=6:1")

    # Test with audio
    audio = create_test_audio()
    with torch.no_grad():
        compressed_audio = compressor(audio)

    print("Frequency-specific compression completed!\n")


def demo_parameter_exploration():
    """Show how to explore and modify compressor parameters."""
    print("=== Parameter Exploration Demo ===")

    compressor = MultiBandCompressor()

    # Show some frequency ranges
    print("Sample frequency ranges for different bands:")
    for band_idx in [0, 100, 500, 1000, 1500, compressor.num_bands-1]:
        low_freq, high_freq = compressor.get_frequency_range(band_idx)
        print(".1f")

    # Show current parameters for a few bands
    print("\nCurrent parameters for first few bands:")
    print("Band | Threshold | Ratio | Makeup Gain")
    print("-----|-----------|-------|-------------")
    for band_idx in range(min(5, compressor.num_bands)):
        print(f"{band_idx:4d} | {compressor.threshold_db[band_idx]:9.1f} | {compressor.ratio[band_idx]:5.1f} | {compressor.makeup_gain_db[band_idx]:11.1f}")

    print("\nParameter exploration completed!\n")


if __name__ == "__main__":
    try:
        demo_basic_compression()
        demo_frequency_specific_compression()
        demo_parameter_exploration()

        print("🎵 All demos completed successfully!")
        print("\nTo use this compressor in your own code:")
        print("1. Install PyTorch: pip install torch")
        print("2. Import: from multiband_compressor import MultiBandCompressor")
        print("3. Create: compressor = MultiBandCompressor()")
        print("4. Process: compressed = compressor(your_audio_tensor)")

    except ImportError as e:
        print(f"Error: {e}")
        print("Please install PyTorch: pip install torch")
    except Exception as e:
        print(f"Unexpected error: {e}")
