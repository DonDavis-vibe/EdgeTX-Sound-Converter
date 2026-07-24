@echo off
echo Building EdgeTX Converter Standalone Executable...
python -m PyInstaller --noconfirm --onefile --windowed --add-data "C:\Users\t-cla\AppData\Roaming\Python\Python312\site-packages\customtkinter;customtkinter/" edgetx_converter.py
echo.
echo Build complete! Your .exe is located in the "dist" folder.
pause
