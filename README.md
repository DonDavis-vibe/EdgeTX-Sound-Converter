# EdgeTX Sound Converter

A sleek, lightweight, cross-platform tool to effortlessly prep, trim, and convert audio files for your EdgeTX radio. Developed by FPV.Davis.

## Features
- **Batch Processing**: Load multiple MP3, WAV, or M4A files at once.
- **Audio Snipping**: Click on any file in your queue to visually trim it. The app remembers your cuts for each individual file.
- **Preview Playback**: Listen to your exact cut before converting, straight from the UI.
- **Auto-Normalization**: Automatically strips dead silence from the start/end and equalizes the volume so all your callouts sound perfect.
- **Strict Format Enforcement**: Automatically converts and renames files to match strict EdgeTX requirements (16kHz, Mono, 16-bit, max 6 characters).
- **High Quality Mode**: An optional bypass switch for modern radios (like the EL18) that support rich 44.1kHz Stereo sound.

## How to Run (For Users)
Simply download the standalone `.exe` from the Releases page (or the `dist` folder). 
**No Python or setup required.** Just double click and use!

## How to Run (For Developers)
If you want to run the python script directly:
```bash
git clone https://github.com/DonDavis-vibe/EdgeTX-Sound-Converter
cd EdgeTX-Sound-Converter
pip install -r requirements.txt
python edgetx_converter.py
```

## Building the Executable
You can easily build your own standalone `.exe` using PyInstaller:
```bash
# Using the provided batch script on Windows
.\build_exe.bat
```

## License
MIT License. Feel free to fork, modify, and distribute!
