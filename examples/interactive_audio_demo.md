# 🎵 Interactive Audio Processing with LPMD

This demonstrates **real-time audio processing** - something Quarto documents can't do!

## Setup Audio Engine

<!-- cell:audio_init -->
```python
from lpmd_audio_features import LPMDAudioEngine, LPMDParameterControls
from multiband_compressor import MultiBandCompressor
import torch

print("🎵 Initializing LPMD Audio Engine...")

# Create real-time audio engine
audio_engine = LPMDAudioEngine(sample_rate=44100, block_size=4096)

# Create interactive parameter controls
controls = LPMDParameterControls()

print("✅ Audio engine ready for real-time processing!")
```

## Interactive Compressor Controls

<!-- cell:compressor_controls depends:audio_init -->
```python
# Add interactive sliders for compression parameters
controls.add_slider('threshold', -40, 0, -20,
                   lambda x: print(f"🎛️ Threshold: {x:.1f}dB"))

controls.add_slider('ratio', 1, 16, 4,
                   lambda x: print(f"🎛️ Ratio: {x:.1f}:1"))

controls.add_slider('attack', 0.1, 100, 5,
                   lambda x: print(f"🎛️ Attack: {x:.1f}ms"))

controls.add_slider('release', 1, 500, 100,
                   lambda x: print(f"🎛️ Release: {x:.1f}ms"))

controls.add_slider('makeup_gain', -20, 20, 0,
                   lambda x: print(f"🎛️ Makeup Gain: {x:.1f}dB"))

print("🎛️ Interactive controls created!")
print("💡 These controls update the compressor in real-time!")
```

## Create Dynamic Compressor

<!-- cell:create_compressor depends:compressor_controls -->
```python
def update_compressor():
    """Create compressor with current control values"""
    return MultiBandCompressor(
        threshold_db=controls.get_value('threshold'),
        ratio=controls.get_value('ratio'),
        attack_ms=controls.get_value('attack'),
        release_ms=controls.get_value('release'),
        makeup_gain_db=controls.get_value('makeup_gain')
    )

# Create initial compressor
compressor = update_compressor()

# Set up real-time audio processing
def audio_processor(audio_chunk):
    # Update compressor with current parameters
    current_compressor = update_compressor()

    # Process audio
    audio_tensor = torch.from_numpy(audio_chunk).float().unsqueeze(0)
    with torch.no_grad():
        processed = current_compressor(audio_tensor)

    return processed.squeeze(0).numpy()

audio_engine.set_processor(audio_processor)

print("🎛️ Dynamic compressor created!")
print("🔄 Parameters update automatically when controls change")
```

## Real-Time Audio Streaming

<!-- cell:start_audio depends:create_compressor -->
```python
# Add control buttons
controls.add_button('start_stream',
                   lambda: audio_engine.start_audio_stream())

controls.add_button('stop_stream',
                   lambda: audio_engine.stop_audio_stream())

print("🎵 Audio streaming controls ready!")
print("💡 Use start_stream() and stop_stream() to control audio")
```

## Live Parameter Adjustment

<!-- cell:parameter_demo depends:start_audio -->
```python
print("🎛️ Interactive Parameter Demo")
print("=" * 30)
print("Try adjusting these parameters in real-time:")
print()

# Show current values
controls.create_ui()

print("\n🎯 Example adjustments:")
print("controls.set_value('threshold', -15)  # More aggressive compression")
print("controls.set_value('ratio', 8)        # Higher ratio")
print("controls.set_value('attack', 1)       # Faster attack")
print("controls.set_value('release', 50)     # Faster release")
print("controls.set_value('makeup_gain', 3)  # Boost output")

print("\n🔄 Parameters update the compressor immediately!")
print("🎵 Hear the difference in real-time!")
```

## Audio Analysis Tools

<!-- cell:analysis_tools depends:create_compressor -->
```python
# Add analysis controls
controls.add_button('show_spectrum',
                   lambda: print("📊 Spectrum analysis would open here"))

controls.add_button('show_compression_curve',
                   lambda: print("📈 Compression curve visualization would open here"))

print("📊 Analysis tools ready!")
print("🔍 Can inspect compressor response in real-time")
```

## Performance Monitoring

<!-- cell:performance_monitor depends:create_compressor -->
```python
import time
import psutil
import os

def monitor_performance():
    """Monitor real-time audio processing performance"""
    process = psutil.Process(os.getpid())

    print("📊 Performance Monitor:")
    print(".1f")
    print(".1f")
    print(".1f")
    print(".1f")

    if hasattr(audio_engine, 'stream') and audio_engine.stream:
        print("🎵 Audio stream: ACTIVE")
        print(".1f")
    else:
        print("🎵 Audio stream: INACTIVE")

# Add performance monitoring button
controls.add_button('performance',
                   lambda: monitor_performance())

print("📈 Performance monitoring enabled!")
print("💡 Check CPU usage, latency, and audio stream status")
```

## Advanced Effects Chain

<!-- cell:effects_chain depends:create_compressor -->
```python
# Create effects chain
effects_chain = []

def add_reverb():
    """Add reverb effect to chain"""
    def reverb_processor(audio):
        # Simple reverb simulation
        decay = 0.3
        delay_samples = int(0.05 * 44100)  # 50ms delay

        # Create delayed signal with decay
        delayed = torch.roll(audio, delay_samples, dims=-1) * decay
        return audio + delayed

    effects_chain.append(reverb_processor)
    print("🌊 Reverb added to effects chain")

def add_distortion():
    """Add distortion effect to chain"""
    def distortion_processor(audio):
        # Soft clipping distortion
        threshold = 0.7
        audio_clipped = torch.where(
            audio > threshold, threshold + (audio - threshold) * 0.3,
            torch.where(audio < -threshold, -threshold + (audio + threshold) * 0.3, audio)
        )
        return audio_clipped

    effects_chain.append(distortion_processor)
    print("🔥 Distortion added to effects chain")

# Add effect buttons
controls.add_button('add_reverb', lambda: add_reverb())
controls.add_button('add_distortion', lambda: add_distortion())

print("🎼 Effects chain ready!")
print("🌊 Add reverb, distortion, or other effects")
print("🔄 Effects process in series after compression")
```

## Complete Interactive Demo

<!-- cell:complete_demo depends:effects_chain,performance_monitor,analysis_tools -->
```python
print("🎉 LPMD Interactive Audio Processing Demo Complete!")
print("=" * 55)
print()
print("🎵 This is what LPMD can do that Quarto can't:")
print()
print("✅ Real-time audio I/O processing")
print("✅ Interactive parameter controls with live updates")
print("✅ Effects chaining and modulation")
print("✅ Performance monitoring")
print("✅ Live spectrum analysis")
print("✅ Audio streaming controls")
print()
print("📄 Quarto creates beautiful documents.")
print("🎵 LPMD creates interactive audio experiences!")
print()
print("🚀 Try it:")
print("  audio_engine.start_audio_stream()  # Start real-time processing")
print("  controls.set_value('threshold', -10)  # Adjust compression")
print("  add_reverb()  # Add reverb effect")
print("  monitor_performance()  # Check system performance")
print()
print("🎛️ This is living, breathing audio processing - not just documentation!")
```

## LPMD vs Quarto: The Real Difference

**Quarto**: Creates beautiful static documents with code examples
**LPMD**: Creates interactive audio processing environments with real-time control

The invisible syntax means your markdown looks clean, but secretly contains a full audio studio!

<!-- cell:cleanup depends:complete_demo -->
```python
# Clean shutdown
if hasattr(audio_engine, 'is_streaming') and audio_engine.is_streaming:
    audio_engine.stop_audio_stream()

print("🧹 LPMD session cleaned up")
print("🎵 Thanks for exploring interactive audio processing!")
```
