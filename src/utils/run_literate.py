#!/usr/bin/env python3
"""
Interactive runner for the 4096-band Multi-Band Compressor Literate Program

This script lets you run the code examples directly from the README.md literate program.
"""

import torch
from multiband_compressor import MultiBandCompressor
import sys

def basic_compression_example():
    """From the 'Basic Compression' section"""
    print("🎵 Basic Compression Example")
    print("=" * 30)

    # Create audio signal (1 second at 44.1kHz)
    audio = torch.randn(1, 1, 44100)
    print(f"Created audio: {audio.shape}")

    # Basic compressor: -20dB threshold, 4:1 ratio
    compressor = MultiBandCompressor(
        threshold_db=-20.0,    # compress when peaks hit -20dB
        ratio=4.0,            # 4:1 compression ratio
        attack_ms=5.0,        # fast attack for transients
        release_ms=100.0,     # slow release for natural sound
        makeup_gain_db=3.0    # boost to compensate for compression
    )

    compressed_audio = compressor(audio)
    print(f"Compressed: {compressed_audio.shape}")
    print("✅ Basic compression completed!")

def frequency_specific_example():
    """From the 'Frequency-Specific Control' section"""
    print("🎵 Frequency-Specific Control Example")
    print("=" * 40)

    compressor = MultiBandCompressor()

    # Customize compression per frequency range
    for band_idx in range(compressor.num_bands):
        low_freq, high_freq = compressor.get_frequency_range(band_idx)

        if low_freq < 200:
            compressor.set_band_parameters(band_idx, threshold_db=-15.0, ratio=2.0)
        elif low_freq < 2000:
            compressor.set_band_parameters(band_idx, threshold_db=-20.0, ratio=4.0)
        else:
            compressor.set_band_parameters(band_idx, threshold_db=-25.0, ratio=3.0)

    print("Applied custom settings for different frequency ranges")

    # Test it
    audio = torch.randn(1, 1, 44100)
    compressed = compressor(audio)
    print(f"Test completed: {audio.shape} → {compressed.shape}")

def inspection_example():
    """From the 'Inspecting the Process' section"""
    print("🎵 Process Inspection Example")
    print("=" * 30)

    # Create a compressor and test audio
    compressor = MultiBandCompressor(threshold_db=-15.0, ratio=4.0, makeup_gain_db=3.0)
    audio = torch.randn(1, 1, 44100)

    result = compressor.process_with_intermediates(audio)

    print("Intermediate results obtained:")
    print(f"  FFT bands: {result['fft_bands'].shape}")
    print(f"  Gain curve: {result['gain_curve_db'].shape}")
    print(f"  Compressed FFT: {result['compressed_fft'].shape}")
    print(f"  Final audio: {result['reconstructed_audio'].shape}")

    # Show some specific bands
    print("\nSample frequency bands:")
    for band_idx in [100, 500, 1000]:
        freq = compressor.get_frequency_range(band_idx)[0]
        mag = result['fft_bands'][band_idx]
        gain = result['gain_curve_db'][band_idx]
        print("4d")

def run_all_demos():
    """Run the complete demo suite"""
    print("🎵 Running Complete Demo Suite")
    print("=" * 35)

    import subprocess
    import sys

    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
        subprocess.run([sys.executable, "fft_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Demo failed: {e}")

def main():
    print("🎵 4096-Band Multi-Band Compressor - Literate Program Runner")
    print("=" * 65)
    print("Choose which part of the literate program to run:")
    print()
    print("1. Basic Compression Example")
    print("2. Frequency-Specific Control Example")
    print("3. Process Inspection Example")
    print("4. Run Complete Demo Suite")
    print("5. Show Quick Start")
    print()
    print("0. Exit")

    while True:
        try:
            choice = input("\nEnter your choice (0-5): ").strip()

            if choice == "0":
                print("Goodbye! 🎵")
                break
            elif choice == "1":
                basic_compression_example()
            elif choice == "2":
                frequency_specific_example()
            elif choice == "3":
                inspection_example()
            elif choice == "4":
                run_all_demos()
            elif choice == "5":
                print("\nQuick Start from the literate program:")
                print("from multiband_compressor import MultiBandCompressor")
                print("compressor = MultiBandCompressor()")
                print("compressed_audio = compressor(your_audio_tensor)")
            else:
                print("Invalid choice. Please enter 0-5.")

        except KeyboardInterrupt:
            print("\nGoodbye! 🎵")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
