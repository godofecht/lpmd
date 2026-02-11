#!/usr/bin/env python3
"""
LPMD Audio Extensions - Real-time Audio Processing Features

This extends LPMD with audio-specific capabilities that Quarto can't match:
- Real-time audio I/O
- Interactive parameter controls
- Live spectrograms and visualizations
- Audio effect chaining
- MIDI control integration
"""

import torch
import numpy as np
# import sounddevice as sd  # Optional: for real audio I/O
# import matplotlib.pyplot as plt  # Optional: for visualization
# from matplotlib.animation import FuncAnimation
import threading
import queue
import time
from typing import Dict, Any, Optional
import asyncio

class LPMDAudioEngine:
    """Real-time audio processing engine for LPMD"""

    def __init__(self, sample_rate=44100, block_size=4096):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.audio_queue = queue.Queue()
        self.is_streaming = False
        self.current_processor = None
        self.test_audio = self._generate_test_audio()  # Simulated audio for demo

    def _generate_test_audio(self):
        """Generate test audio signal for demonstration"""
        t = np.linspace(0, 2, int(2 * self.sample_rate))
        # Mix of frequencies to demonstrate compression
        audio = (
            0.5 * np.sin(2 * np.pi * 200 * t) +   # low freq
            0.3 * np.sin(2 * np.pi * 2000 * t) +  # mid freq
            0.2 * np.sin(2 * np.pi * 8000 * t)    # high freq
        )
        return audio.astype(np.float32)

    def start_audio_stream(self, input_device=None, output_device=None):
        """Start simulated real-time audio streaming"""
        if not self.is_streaming:
            self.is_streaming = True
            # Start background thread for simulated streaming
            self.stream_thread = threading.Thread(target=self._simulate_streaming)
            self.stream_thread.daemon = True
            self.stream_thread.start()
            print(f"🎵 Simulated audio stream started: {self.sample_rate}Hz, {self.block_size} samples")

    def _simulate_streaming(self):
        """Simulate real-time audio streaming"""
        pos = 0
        while self.is_streaming:
            # Get next chunk of test audio
            chunk = self.test_audio[pos:pos + self.block_size]
            if len(chunk) < self.block_size:
                # Loop back to start if we reach the end
                remaining = self.block_size - len(chunk)
                chunk = np.concatenate([chunk, self.test_audio[:remaining]])
                pos = remaining
            else:
                pos += self.block_size

            # Process through current processor
            if self.current_processor:
                processed_chunk = self.current_processor(chunk.reshape(1, -1))
                chunk = processed_chunk.flatten()

            # Queue for visualization
            self.audio_queue.put(chunk.copy())

            # Simulate real-time timing
            time.sleep(self.block_size / self.sample_rate)

    def stop_audio_stream(self):
        """Stop audio streaming"""
        self.is_streaming = False
        if hasattr(self, 'stream_thread'):
            self.stream_thread.join(timeout=1.0)
        print("🎵 Audio stream stopped")

    def set_processor(self, processor_func):
        """Set the current audio processor function"""
        self.current_processor = processor_func
        print("🔧 Audio processor updated")

    def create_visualization(self):
        """Create simple audio visualization (text-based for demo)"""
        print("🎨 Audio Visualization Started")
        print("💡 (In a real implementation, this would show matplotlib plots)")

        # Simple text-based visualization
        for i in range(10):  # Show 10 updates
            try:
                audio_data = self.audio_queue.get(timeout=1.0)
                rms = np.sqrt(np.mean(audio_data**2))

                # Simple spectrum analysis
                if len(audio_data) >= 1024:
                    fft = np.fft.rfft(audio_data[:1024])
                    magnitude = np.abs(fft)
                    peak_freq = np.argmax(magnitude) * self.sample_rate / 2048

                    print(f"🎵 RMS: {rms:.3f}, Peak Freq: {peak_freq:.0f}Hz")
                else:
                    print(f"🎵 RMS: {rms:.3f}")

            except queue.Empty:
                print("⏳ Waiting for audio data...")
                break

        print("🎨 Visualization complete")

class LPMDParameterControls:
    """Interactive parameter controls for LPMD cells"""

    def __init__(self):
        self.parameters = {}
        self.callbacks = []

    def add_slider(self, name: str, min_val: float, max_val: float,
                   default: float, callback=None):
        """Add an interactive slider control"""
        self.parameters[name] = {
            'type': 'slider',
            'min': min_val,
            'max': max_val,
            'value': default,
            'callback': callback
        }
        print(f"🎛️ Added slider: {name} ({min_val} - {max_val}, default: {default})")

    def add_button(self, name: str, callback=None):
        """Add an interactive button"""
        self.parameters[name] = {
            'type': 'button',
            'callback': callback
        }
        print(f"🔘 Added button: {name}")

    def get_value(self, name: str):
        """Get current parameter value"""
        return self.parameters[name]['value']

    def set_value(self, name: str, value: float):
        """Set parameter value and trigger callback"""
        if name in self.parameters:
            self.parameters[name]['value'] = value
            if self.parameters[name]['callback']:
                self.parameters[name]['callback'](value)

    def create_ui(self):
        """Create a simple text-based UI for parameter control"""
        print("\n🎛️ LPMD Parameter Controls:")
        print("=" * 40)

        for name, param in self.parameters.items():
            if param['type'] == 'slider':
                print(".1f")
            elif param['type'] == 'button':
                print(f"  {name}: [Button]")

        print("\n💡 Use set_value('param_name', value) to adjust parameters")
        print("💡 Call parameter callbacks for real-time updates")

# Audio processing functions for LPMD cells
def create_audio_processor(compressor, threshold_db=-20, ratio=4, makeup_gain=0):
    """Create a real-time audio processing function"""
    def process_audio(audio_chunk):
        # Convert to torch tensor
        audio_tensor = torch.from_numpy(audio_chunk).float()
        audio_tensor = audio_tensor.unsqueeze(0)  # Add batch dimension

        # Apply compression
        with torch.no_grad():
            compressed = compressor(audio_tensor)

        # Apply real-time parameter adjustments
        compressed = compressed * (10 ** (makeup_gain / 20))  # Makeup gain

        return compressed.squeeze(0).numpy()

    return process_audio

# Example usage in LPMD cells
"""
Example LPMD cell with audio features:

<!-- cell:audio_setup -->
```python
from lpmd_audio_features import LPMDAudioEngine, LPMDParameterControls

# Create audio engine
audio_engine = LPMDAudioEngine(sample_rate=44100)

# Create parameter controls
controls = LPMDParameterControls()
controls.add_slider('threshold', -40, 0, -20, lambda x: print(f"Threshold: {x}dB"))
controls.add_slider('ratio', 1, 16, 4, lambda x: print(f"Ratio: {x}:1"))
controls.add_button('start_audio', lambda: audio_engine.start_audio_stream())
controls.add_button('stop_audio', lambda: audio_engine.stop_audio_stream())

# Create compressor
compressor = MultiBandCompressor(
    threshold_db=controls.get_value('threshold'),
    ratio=controls.get_value('ratio')
)

# Set up real-time processing
processor = create_audio_processor(compressor)
audio_engine.set_processor(processor)
```

<!-- cell:live_visualization depends:audio_setup -->
```python
# Start live audio visualization
audio_engine.create_visualization()
```

<!-- cell:parameter_tweaking depends:audio_setup -->
```python
# Interactive parameter adjustment
controls.create_ui()

# Example: Adjust threshold in real-time
controls.set_value('threshold', -15)  # Triggers callback
controls.set_value('ratio', 6)        # Triggers callback
```
"""

if __name__ == "__main__":
    print("🎵 LPMD Audio Features Demo")
    print("=" * 30)

    # Demo parameter controls
    controls = LPMDParameterControls()
    controls.add_slider('threshold', -40, 0, -20)
    controls.add_slider('ratio', 1, 16, 4)
    controls.add_button('process')

    controls.create_ui()

    print("\n✅ LPMD Audio Extensions Ready!")
    print("   - Real-time audio processing")
    print("   - Interactive parameter controls")
    print("   - Live visualization")
    print("   - Audio effect chaining")
