# 📻 EdgeTX Sound Converter

![GitHub License](https://img.shields.io/github/license/DonDavis-vibe/EdgeTX-Sound-Converter)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)

A sleek, standalone tool built by **FPV.Davis** to effortlessly prep, trim, and convert audio files for your EdgeTX radio (and modern radios like the EL18). 

Tired of manually messing with Audacity just to get a 16kHz Mono WAV file with a 6-character name? This app automates everything. Just drop in your favorite songs, sound bites, or voice clips, and let the converter handle the rest.

---

## ✨ Key Features

- ✂️ **Visual Batch Snipping**: Select exactly what part of a song you want. The app remembers your custom slider cuts for *each individual file* in your batch!
- 🔈 **Live Audio Preview**: Listen to your trimmed snippets instantly before you commit to converting.
- 🎚️ **Smart Auto-Normalization**: Automatically strips dead silence from the beginning and end of clips, and normalizes the volume so all your callouts match perfectly on the flight line.
- 🎯 **Strict Format Enforcement**: Automatically converts anything (MP3, WAV, M4A, etc.) to the strict EdgeTX requirements: `16kHz`, `Mono`, `16-bit`, and standardizes the filename to max `6 characters`.
- 🎧 **High Quality Bypass**: Have a modern radio (like the FlySky EL18)? Switch to "High Quality" mode to export rich `44.1kHz Stereo` sound instead!
- 📦 **100% Standalone**: No Python, no dependencies, no FFmpeg installs needed. Just run the `.exe`.

---

## 🚀 Installation & Usage

### 🪟 Windows (Easiest)
1. Head over to the **Releases** tab on GitHub.
2. Download `edgetx_converter_fixed.exe` (or whatever the latest version is named).
3. Double-click to run! *(Note: The very first time it runs, it will silently download the necessary FFmpeg audio engines in the background so you don't have to).*

### 🍏 macOS & 🐧 Linux
Because this tool is built with Python and CustomTkinter, it runs natively on any OS!
1. Ensure you have Python 3 installed.
2. Clone this repository: `git clone https://github.com/DonDavis-vibe/EdgeTX-Sound-Converter`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the app: `python edgetx_converter.py`

### 🎛️ How to Use
1. Click **Select Audio Files** and pick any songs or voice clips you want to use.
5. *(Optional)* Click on a file in the list and use the sliders to **trim** a specific section. Hit **Preview Cut** to listen!
6. Select your output quality (Standard is safest for older radios).
7. Click **Convert All Files** and pick where you want to save them (e.g., straight to your radio's SD card `SOUNDS/en` folder!).

---

## 💻 Development Setup

Want to tweak the code, change the UI, or build it yourself?

### Setup
```bash
git clone https://github.com/DonDavis-vibe/EdgeTX-Sound-Converter
cd EdgeTX-Sound-Converter
pip install -r requirements.txt
python edgetx_converter.py
```

### Building the Standalone `.exe` (Windows)
We use PyInstaller to bundle the app into a single executable. A quick batch script is included for convenience:
```bash
.\build_exe.bat
```
*(Mac and Linux users can also run `PyInstaller` manually to create `.app` or Linux binaries).*

---

## 📜 License & Credits

Distributed under the MIT License. Feel free to fork, modify, and distribute!
Built for the FPV and RC community by **FPV.Davis**.
