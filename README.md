# EdgeTX Sound Converter

A modern, cross-platform Python GUI application for converting any audio file (MP3, WAV, M4A, etc.) into the strict format required by EdgeTX radios.

## Features

- **No-Hassle Dependencies**: Uses `imageio-ffmpeg` to automatically download and manage FFmpeg in the background. No manual FFmpeg installation required!
- **EdgeTX Safe**: Automatically converts audio to 16-bit PCM WAV.
- **Selectable Quality**:
  - **Standard**: 16kHz Mono (Safest format, strict EdgeTX official spec, takes up minimal space).
  - **High Quality**: 44.1kHz Stereo (Rich sound for newer radios like the Flysky EL18).
- **Auto-trimming**: Detects and trims absolute digital silence from the start and end of your clips so callouts play instantly.
- **Volume Normalization**: Normalizes all clips to `-10 dBFS` so your radio sounds uniformly loud.
- **Filename Sanitization**: Automatically renames files to be all lowercase, replaces spaces with underscores, and strictly truncates to 6 characters to guarantee flawless EdgeTX compatibility.
- **Cross-Platform**: Works natively on Windows, macOS, and Linux.

## Installation

1. Ensure you have [Python 3.7+](https://www.python.org/downloads/) installed.
2. Clone or download this repository.
3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from your terminal:

```bash
python edgetx_converter.py
```

1. Click **Select Audio Files** to choose your MP3s or WAVs.
2. Select your desired output quality.
3. Click **Convert Files** and choose a folder to save your new sounds.
4. Drag and drop the converted sounds into your radio's SD card (usually `SOUNDS/en/`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
