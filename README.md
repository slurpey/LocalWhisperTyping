# LocalWhisperTyping

A robust voice-to-text application for Windows that uses OpenAI's Whisper model to convert speech to text in real-time. Simply hold Ctrl+Shift to record your voice, release to automatically type the transcribed text into any active application.

## Features

- **Real-time Voice Typing**: Hold Ctrl+Shift to record, release to type
- **OpenAI Whisper Integration**: High-quality speech recognition using the Whisper "base" model
- **System Tray Integration**: Runs quietly in the background with system tray icon
- **Robust Keyboard Hook Management**: Self-monitoring and auto-recovery of keyboard shortcuts
- **Audio Device Management**: Automatic detection and validation of audio input devices
- **Window Focus Restoration**: Automatically returns focus to the original application after typing
- **Comprehensive Logging**: Detailed logging for troubleshooting and monitoring
- **Silence Detection**: Intelligent filtering of empty or silent recordings

## System Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **Audio**: Working microphone/audio input device
- **Memory**: At least 2GB RAM (Whisper model requires ~1GB)
- **Storage**: ~500MB for Whisper model files

## Installation

### 🔰 For Absolute Beginners
**New to programming?** Follow the complete step-by-step guide: **[BEGINNER_SETUP.md](BEGINNER_SETUP.md)**

This guide includes:
- Installing Python from scratch
- Setting up all components
- Troubleshooting common issues
- No programming knowledge required

### 🚀 For Experienced Users

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/slurpey/LocalWhisperTyping.git
   cd LocalWhisperTyping
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **First Run Setup**:
   On first launch, Whisper will download the base model (~150MB). This may take a few minutes.

## Usage

### Easy Startup (Recommended)

**Double-click `start_voice_typing.bat`** - This batch file provides the easiest way to start the application:
- Automatically changes to the correct directory
- Activates virtual environment if present
- Starts the voice typing service with helpful status messages
- Keeps the window open if errors occur for troubleshooting

### Manual Startup

1. **Start the Application**:
   ```bash
   python lloydswhisper.py
   ```

2. **Voice Typing**:
   - Hold `Ctrl+Shift` to start recording
   - Speak clearly into your microphone
   - Release `Ctrl+Shift` to stop recording and automatically type the transcribed text

3. **Exit Application**:
   - Press `Ctrl+Shift+Esc` to quit
   - Or right-click the system tray icon and select "Quit"

### System Tray Features

The application runs with a microphone icon in your system tray with the following options:
- **Show Status**: Display current service status and activity
- **Restart Hooks**: Manually restart keyboard hooks if they become unresponsive
- **Open Log**: View the detailed log file
- **Quit**: Close the application

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift` (hold) | Record voice and transcribe on release |
| `Ctrl+Shift+Esc` | Exit application |

## How It Works

1. **Recording**: When you press Ctrl+Shift, the application starts recording audio from your default microphone
2. **Processing**: Upon release, the audio is processed through OpenAI's Whisper model for speech recognition
3. **Typing**: The transcribed text is automatically typed into whatever application currently has focus
4. **Cleanup**: Temporary audio files are automatically cleaned up

## Configuration

### Audio Settings
- **Sample Rate**: 16kHz (optimized for Whisper)
- **Channels**: Mono
- **Format**: 32-bit float during recording, 16-bit WAV for processing
- **Maximum Recording Time**: 90 seconds per session

### Whisper Model
- **Default Model**: `base` (good balance of speed and accuracy)
- **Alternative Models**: You can modify the code to use `tiny`, `small`, `medium`, or `large` models
  - `tiny`: Fastest, least accurate
  - `base`: Good balance (default)
  - `small`: Better accuracy, slower
  - `medium`: Even better accuracy, much slower
  - `large`: Best accuracy, very slow

## Troubleshooting

### Common Issues

**Keyboard shortcuts not working:**
- Try the "Restart Hooks" option from the system tray menu
- Check if another application is interfering with global hotkeys
- Restart the application

**No audio detected:**
- Verify your microphone is working in other applications
- Check Windows audio settings and permissions
- Ensure your microphone is set as the default recording device

**Transcription is inaccurate:**
- Speak clearly and at a moderate pace
- Reduce background noise
- Ensure your microphone is positioned correctly
- Consider upgrading to a larger Whisper model

**Application crashes or becomes unresponsive:**
- Check the log file (`voice_typing.log`) for error details
- Ensure all dependencies are properly installed
- Try running with administrator privileges

### Performance Optimization

- **Close unnecessary applications** to free up RAM for Whisper processing
- **Use a good quality microphone** for better recognition accuracy
- **Speak in quiet environments** to minimize background noise
- **Keep recordings under 30 seconds** for optimal processing speed

## Development

### Project Structure
```
LocalWhisperTyping/
├── lloydswhisper.py        # Main application
├── start_voice_typing.bat  # Easy startup script (Windows)
├── README.md               # Technical documentation (this file)
├── BEGINNER_SETUP.md       # Complete beginner's installation guide
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore patterns
├── LICENSE                # MIT License
└── voice_typing.log       # Generated log file (created on first run)
```

### What is a .bat file?
A `.bat` (batch) file is a Windows script that automates command-line operations. The `start_voice_typing.bat` file:
- **Simplifies startup**: Just double-click instead of opening terminal and typing commands
- **Handles errors**: Shows error messages if something goes wrong
- **Virtual environment support**: Automatically activates Python virtual environments if present
- **User-friendly**: Displays helpful information about controls and usage
- **Directory management**: Ensures the script runs from the correct location

### Key Components
- **Audio Recording**: Uses `sounddevice` for real-time audio capture
- **Speech Recognition**: OpenAI Whisper for transcription
- **Keyboard Handling**: `keyboard` library for global hotkeys
- **System Tray**: `pystray` for background operation
- **Window Management**: Windows API for focus restoration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the excellent speech recognition model
- [sounddevice](https://python-sounddevice.readthedocs.io/) for audio recording capabilities
- [keyboard](https://github.com/boppreh/keyboard) for global hotkey support
- [pystray](https://github.com/moses-palmer/pystray) for system tray integration

## Changelog

### Version 1.0.0
- Initial release with core voice typing functionality
- System tray integration
- Robust keyboard hook management
- Comprehensive logging and error handling
- Audio device validation and management
