# Literate Python Markdown (.lpmd) Demo

This is a demonstration of **Literate Python Markdown** - a new markdown-based format for executable literate programs.

## Cell-Based Execution

<!-- cell:init -->
```python
# Initialize the environment
import torch
from multiband_compressor import MultiBandCompressor
import numpy as np

print("🎵 Literate Python Markdown Environment Ready!")
print(f"PyTorch version: {torch.__version__}")
```
<!-- cell:create_audio depends:init -->
```python
# Create test audio signal
sample_rate = 44100
duration = 1.0
t = torch.linspace(0, duration, int(sample_rate * duration))

# Mix of frequencies
audio = (
    0.5 * torch.sin(2 * torch.pi * 200 * t) +   # low freq
    0.3 * torch.sin(2 * torch.pi * 2000 * t) +  # mid freq
    0.2 * torch.sin(2 * torch.pi * 8000 * t)    # high freq
)

# Normalize and add dimensions
audio = audio / torch.max(torch.abs(audio))
audio = audio.unsqueeze(0).unsqueeze(0)

print(f"Created audio signal: {audio.shape}")
```
<!--
<!-- cell:compressor depends:create_audio persist:compressor -->
```python
# Create multi-band compressor
compressor = MultiBandCompressor(
    threshold_db=-15.0,
    ratio=4.0,
    attack_ms=5.0,
    release_ms=50.0,
    makeup_gain_db=3.0
)

print(f"Compressor created with {compressor.num_bands} frequency bands")
```
<!--
<!-- cell:frequency_control depends:compressor persist:compressor -->
```python
# Set different compression for different frequencies
bands_modified = {'low': 0, 'mid': 0, 'high': 0}

for band_idx in range(compressor.num_bands):
    low_freq, high_freq = compressor.get_frequency_range(band_idx)

    if low_freq < 200:
        compressor.set_band_parameters(band_idx, threshold_db=-15.0, ratio=2.0)
        bands_modified['low'] += 1
    elif low_freq < 2000:
        compressor.set_band_parameters(band_idx, threshold_db=-20.0, ratio=4.0)
        bands_modified['mid'] += 1
    else:
        compressor.set_band_parameters(band_idx, threshold_db=-25.0, ratio=6.0)
        bands_modified['high'] += 1

print("Frequency-specific settings applied:")
for freq_range, count in bands_modified.items():
    print(f"  {freq_range}: {count} bands")
```
<!--
<!-- cell:compression depends:compressor,frequency_control -->
```python
# Apply compression
with torch.no_grad():
    compressed_audio = compressor(audio)

print(f"Original audio shape: {audio.shape}")
print(f"Compressed audio shape: {compressed_audio.shape}")

# Calculate some statistics
original_rms = torch.sqrt(torch.mean(audio**2))
compressed_rms = torch.sqrt(torch.mean(compressed_audio**2))

print(f"Original RMS: {original_rms:.4f}")
print(f"Compressed RMS: {compressed_rms:.4f}")
print(f"Compression ratio: {original_rms/compressed_rms:.2f}x")
```
<!--
<!-- cell:intermediates depends:compressor -->
```python
# Examine the compression process in detail
result = compressor.process_with_intermediates(audio)

print("Intermediate compression results:")
print(f"  FFT bands: {result['fft_bands'].shape}")
print(f"  Gain curve: {result['gain_curve_db'].shape}")
print(f"  Compressed FFT: {result['compressed_fft'].shape}")

# Show compression for specific frequencies
print("\nCompression analysis for specific bands:")
for band_idx in [100, 500, 1000]:
    freq = compressor.get_frequency_range(band_idx)[0]
    original_mag = result['fft_bands'][band_idx]
    gain_reduction = result['gain_curve_db'][band_idx]
    print("4d")
```
<!--

## Interactive Elements

<!-- cell:plot_data depends:intermediates -->
```python
# Prepare data for visualization
freq_bins = torch.fft.rfftfreq(4096, 1.0/44100)[:2049]
fft_magnitudes = result['fft_bands']
gain_reductions = result['gain_curve_db']

# Convert tensors to numpy for visualization
plot_data = {
    'frequencies': freq_bins.detach().numpy(),
    'magnitudes': fft_magnitudes.detach().numpy(),
    'gains_db': gain_reductions.detach().numpy()
}

print(f"Prepared plotting data: {len(plot_data)} datasets")
print(f"Frequency range: {freq_bins[0]:.1f}Hz to {freq_bins[-1]:.1f}Hz")
print(f"Sample data points: {len(plot_data['frequencies'])}")
```
<!--
<!-- cell:summary depends:compression,intermediates -->
```python
print("🎵 Literate Python Markdown Demo Complete!")
print("=" * 50)
print("Executed cells in dependency order:")
print("  ✓ init - Environment setup")
print("  ✓ create_audio - Audio signal generation")
print("  ✓ compressor - Multi-band compressor creation")
print("  ✓ frequency_control - Per-band parameter setting")
print("  ✓ compression - Audio compression")
print("  ✓ intermediates - Process analysis")
print("  ✓ plot_data - Visualization data prep")
print("  ✓ summary - Final results")
print()
print(f"Final result: {audio.shape} → {compressed_audio.shape}")
print("✅ Literate Python Markdown execution successful!")
```
---
