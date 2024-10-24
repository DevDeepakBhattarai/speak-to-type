# Real-time Speech-to-Text Transcriber

A Python application that performs real-time speech transcription using Faster Whisper and automatically types the transcribed text wherever your cursor is focused. Perfect for dictation, note-taking, or accessibility purposes.

## Features

- Real-time speech transcription
- Automatic text input at cursor location
- GPU acceleration support (CUDA)
- Voice Activity Detection (VAD) to reduce false positives
- Simple F2 toggle to start/stop transcription

## Requirements

- Python 3.8 or higher
- NVIDIA GPU with CUDA support (optional, but recommended)
- Microphone

## Installation

1. Clone this repository or download the script:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python main.py
```

2. Controls:
- Press `F2` to start/stop transcription
- Press `Ctrl+C` to exit the program
- Place your cursor where you want the text to appear

## Configuration

The script uses these default settings:
- Model: "small" (good balance of speed and accuracy)
- Sample rate: 16000 Hz
- Chunk duration: 2 seconds
- Language: English

## Troubleshooting

### OpenMP Error
If you see an OpenMP error, don't worry - it's handled by the script and won't affect functionality.

### No Audio Input
Make sure your microphone is:
1. Connected
2. Set as the default input device
3. Has proper permissions enabled

### GPU Issues
- Ensure you have CUDA installed if using an NVIDIA GPU
- Check that PyTorch is installed with CUDA support

## Dependencies

- faster-whisper: Speech recognition model
- numpy: Numerical processing
- sounddevice: Audio input handling
- pyautogui: Automatic text input
- keyboard: Hotkey handling
- torch: PyTorch for GPU acceleration

## Performance Notes

- GPU usage with CUDA provides significantly better performance
- The "small" model offers a good balance between accuracy and speed
- Adjusting chunk_duration in the code can help with latency vs accuracy

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Uses OpenAI's Whisper model architecture
- Faster Whisper implementation for improved performance
- Built with Python and PyTorch