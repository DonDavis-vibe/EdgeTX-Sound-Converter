import os
import sys
import re
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Fix for PyInstaller --windowed mode (sys.stdout is None)
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

# Add ffmpeg and ffprobe to PATH so pydub can read MP3s
import static_ffmpeg
static_ffmpeg.add_paths()
from pydub import AudioSegment

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EdgeTXConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EdgeTX Sound Converter")
        self.geometry("700x820")
        self.configure(fg_color="#1a1a1a") # Very dark, sleek background
        
        self.files_data = {}
        self.current_edit_file = None
        self.loaded_audio_cache = {}
        
        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(30, 20), fill="x")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="EdgeTX Sound Converter", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack()
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Easily prep and trim audio for your radio", font=ctk.CTkFont(size=14), text_color="gray")
        self.subtitle_label.pack()
        
        self.help_btn = ctk.CTkButton(self.header_frame, text="💡 SD Card & Radio Setup Guide", command=self.show_help_modal, fg_color="#3a7ebf", hover_color="#1f538d", height=32, font=ctk.CTkFont(size=13, weight="bold"))
        self.help_btn.pack(pady=(10, 0))
        
        # --- Main Content Frame ---
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=20)
        
        # --- File Selection Section ---
        self.file_frame = ctk.CTkFrame(self.main_scroll, corner_radius=15, fg_color="#242424")
        self.file_frame.pack(pady=10, fill="x", ipady=10)
        
        self.select_btn = ctk.CTkButton(self.file_frame, text="📂 Select Audio Files", command=self.select_files, font=ctk.CTkFont(size=15, weight="bold"), corner_radius=8, height=40)
        self.select_btn.pack(pady=(20, 10))
        
        self.file_list_frame = ctk.CTkScrollableFrame(self.file_frame, width=580, height=130, fg_color="#1e1e1e", corner_radius=10)
        self.file_list_frame.pack(pady=10, padx=20)
        
        self.no_files_label = ctk.CTkLabel(self.file_list_frame, text="No files selected.", text_color="gray")
        self.no_files_label.pack(pady=50)
        
        # --- Options Section ---
        self.options_frame = ctk.CTkFrame(self.main_scroll, corner_radius=15, fg_color="#242424")
        self.options_frame.pack(pady=10, fill="x")
        
        self.opt_label = ctk.CTkLabel(self.options_frame, text="Output Quality Profile", font=ctk.CTkFont(size=16, weight="bold"))
        self.opt_label.pack(pady=(15, 5))
        
        self.quality_var = ctk.StringVar(value="standard")
        
        self.radio_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.radio_frame.pack(pady=(5, 15))
        
        self.rad_standard = ctk.CTkRadioButton(self.radio_frame, text="Standard EdgeTX\n(16kHz, Mono, 6 chars)", variable=self.quality_var, value="standard", font=ctk.CTkFont(size=13))
        self.rad_standard.grid(row=0, column=0, padx=20)
        
        self.rad_hq = ctk.CTkRadioButton(self.radio_frame, text="High Quality (EL18)\n(44.1kHz, Stereo)", variable=self.quality_var, value="hq", font=ctk.CTkFont(size=13))
        self.rad_hq.grid(row=0, column=1, padx=20)

        # --- Trimming Section ---
        self.trim_frame = ctk.CTkFrame(self.main_scroll, corner_radius=15, fg_color="#242424")
        self.trim_frame.pack(pady=10, fill="x")
        
        self.trim_title = ctk.CTkLabel(self.trim_frame, text="Audio Snipping", font=ctk.CTkFont(size=16, weight="bold"))
        self.trim_title.pack(pady=(15, 5))
        
        self.trim_subtitle = ctk.CTkLabel(self.trim_frame, text="Click a file in the list above to trim it", text_color="gray", font=ctk.CTkFont(size=12))
        self.trim_subtitle.pack(pady=(0, 10))
        
        self.slider_frame = ctk.CTkFrame(self.trim_frame, fg_color="transparent")
        self.slider_frame.pack(fill="x", padx=20, pady=5)
        
        self.start_label = ctk.CTkLabel(self.slider_frame, text="Start: 0.0s", width=80, anchor="w")
        self.start_label.grid(row=0, column=0, padx=5)
        self.start_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=10, command=self.on_start_slider_move, state="disabled", button_color="#3a7ebf", progress_color="#3a7ebf")
        self.start_slider.set(0)
        self.start_slider.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.slider_frame.columnconfigure(1, weight=1)
        
        self.end_label = ctk.CTkLabel(self.slider_frame, text="End: 0.0s", width=80, anchor="w")
        self.end_label.grid(row=1, column=0, padx=5)
        self.end_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=10, command=self.on_end_slider_move, state="disabled", button_color="#3a7ebf", progress_color="#3a7ebf")
        self.end_slider.set(10)
        self.end_slider.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        
        self.preview_btn = ctk.CTkButton(self.trim_frame, text="▶ Preview Cut", command=self.preview_audio, state="disabled", fg_color="gray", corner_radius=8, font=ctk.CTkFont(weight="bold"))
        self.preview_btn.pack(pady=(10, 20))
        
        # --- Conversion Action ---
        self.convert_btn = ctk.CTkButton(self.main_scroll, text="Convert All Files", command=self.start_conversion, font=ctk.CTkFont(size=18, weight="bold"), fg_color="#2eb82e", hover_color="#248f24", height=50, corner_radius=10)
        self.convert_btn.pack(pady=20, fill="x")
        
        # --- Log Output ---
        self.log_textbox = ctk.CTkTextbox(self.main_scroll, height=100, corner_radius=10, fg_color="#1e1e1e", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.pack(pady=(0, 20), fill="x")
        self.log_textbox.insert("0.0", "System ready.\n")
        self.log_textbox.configure(state="disabled")
        
        # --- Footer ---
        self.footer_label = ctk.CTkLabel(self.main_scroll, text="by FPV.Davis", font=ctk.CTkFont(size=10, slant="italic"), text_color="gray50")
        self.footer_label.pack(pady=(0, 10))

    def show_help_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("EdgeTX Sound Setup Guide")
        modal.geometry("620x560")
        modal.configure(fg_color="#1a1a1a")
        modal.transient(self)
        modal.grab_set()
        
        scroll = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(scroll, text="📖 SD Card & Radio Setup Guide", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3a7ebf")
        title.pack(pady=(0, 15), anchor="w")
        
        help_text = """where to put your converted files:

1. 📂 SD Card File Location
The startup sound and custom audio prompts for EdgeTX radios are stored on your radio's SD card. You will find or place the files at the following path:
👉 SD Card/SOUNDS/<language_code>/ (e.g., SD Card/SOUNDS/en/)

If you are replacing built-in system sounds (like the startup greeting 'hello.wav'):
👉 SD Card/SOUNDS/<language_code>/SYSTEM/hello.wav

For example, if your radio is set to English:
SD Card/SOUNDS/en/SYSTEM/hello.wav

---

2. 🎮 Custom Audio for Specific Buttons / Switches
If you want a specific sound file or custom voice line to play whenever you flip a switch or press a button while using a model:

• Press the MDL (or MODEL) button to open Model Setup.
• Page over to SPECIAL FUNCTIONS (or LOGICAL SWITCHES / SPECIAL FX depending on your screen/theme).
• Add a new function:
    - Switch: Move the switch or press the button you want to trigger the sound (e.g., SA↓).
    - Action: Select 'Play Sound' (for built-in beeps) or 'Play Track' (to pick a .wav file from your SD card).
    - Parameters: Choose the beep pattern or select your target sound file.

⚠️ Note: If key sounds still aren't playing after adjusting the volume, double-check that your master volume slider/potentiometer assigned in Radio Setup isn't turned all the way down."""
        
        label = ctk.CTkLabel(scroll, text=help_text, font=ctk.CTkFont(size=13), justify="left", wraplength=550)
        label.pack(anchor="w", pady=5)
        
        close_btn = ctk.CTkButton(modal, text="Close Guide", command=modal.destroy, fg_color="#2eb82e", hover_color="#248f24", height=40, font=ctk.CTkFont(size=15, weight="bold"))
        close_btn.pack(pady=15)

    def log(self, message):
        def _log():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", message + "\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")
        self.after(0, _log)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=(("Audio Files", "*.mp3 *.wav *.m4a *.ogg *.flac *.aac"), ("All Files", "*.*"))
        )
        if not files:
            return
            
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
            
        self.files_data = {}
        self.current_edit_file = None
        self.loaded_audio_cache = {}
        
        self.start_slider.configure(state="disabled")
        self.end_slider.configure(state="disabled")
        self.preview_btn.configure(state="disabled", fg_color="gray")
        self.trim_subtitle.configure(text="Click a file in the list above to trim it")

        for f in files:
            btn = ctk.CTkButton(
                self.file_list_frame, 
                text=os.path.basename(f), 
                anchor="w", 
                fg_color="transparent", 
                text_color="gray80",
                hover_color="#333333",
                corner_radius=5,
                font=ctk.CTkFont(size=13),
                command=lambda filepath=f: self.select_file_for_editing(filepath)
            )
            btn.pack(fill="x", pady=2, padx=5)
            
            self.files_data[f] = {
                "button": btn,
                "duration": None,
                "start": 0.0,
                "end": 0.0,
                "edited": False,
                "basename": os.path.basename(f)
            }
            
        self.log(f"Loaded {len(files)} files into queue.")

    def select_file_for_editing(self, filepath):
        for f, data in self.files_data.items():
            if data["edited"]:
                data["button"].configure(fg_color="transparent", text_color="#2eb82e") # Green for edited
            else:
                data["button"].configure(fg_color="transparent", text_color="gray80")
            
        self.files_data[filepath]["button"].configure(fg_color="#3a7ebf", text_color="white") # Blue for active
        self.current_edit_file = filepath
        self.trim_subtitle.configure(text=f"Editing: {self.files_data[filepath]['basename']}")
        
        if self.files_data[filepath]["duration"] is None:
            self.log(f"Caching {self.files_data[filepath]['basename']}...")
            threading.Thread(target=self._load_audio_for_edit, args=(filepath,), daemon=True).start()
        else:
            self._update_sliders_for_current_file()

    def _load_audio_for_edit(self, filepath):
        try:
            audio = AudioSegment.from_file(filepath)
            duration_s = len(audio) / 1000.0
            self.loaded_audio_cache[filepath] = audio
            
            self.files_data[filepath]["duration"] = duration_s
            self.files_data[filepath]["start"] = 0.0
            self.files_data[filepath]["end"] = duration_s
            
            if self.current_edit_file == filepath:
                self.after(0, self._update_sliders_for_current_file)
        except Exception as e:
            self.after(0, lambda: self.log(f"[ERROR] Could not load {self.files_data[filepath]['basename']}: {e}"))

    def _update_sliders_for_current_file(self):
        data = self.files_data[self.current_edit_file]
        duration_s = data["duration"]
        
        self.start_slider.configure(state="normal", to=duration_s)
        self.end_slider.configure(state="normal", to=duration_s)
        self.preview_btn.configure(state="normal", fg_color=["#3a7ebf", "#1f538d"])
        
        self.start_slider.set(data["start"])
        self.end_slider.set(data["end"])
        
        self.start_label.configure(text=f"Start: {data['start']:.1f}s")
        self.end_label.configure(text=f"End: {data['end']:.1f}s")

    def on_start_slider_move(self, value):
        if not self.current_edit_file: return
        if value > self.end_slider.get():
            self.start_slider.set(self.end_slider.get() - 0.1)
            value = self.start_slider.get()
            
        self.start_label.configure(text=f"Start: {value:.1f}s")
        self.mark_file_edited(self.current_edit_file, start=value)

    def on_end_slider_move(self, value):
        if not self.current_edit_file: return
        if value < self.start_slider.get():
            self.end_slider.set(self.start_slider.get() + 0.1)
            value = self.end_slider.get()
            
        self.end_label.configure(text=f"End: {value:.1f}s")
        self.mark_file_edited(self.current_edit_file, end=value)

    def mark_file_edited(self, filepath, start=None, end=None):
        data = self.files_data[filepath]
        if start is not None: data["start"] = start
        if end is not None: data["end"] = end
        
        is_edited = (data["start"] > 0.1) or (data["end"] < data["duration"] - 0.1)
        data["edited"] = is_edited
        
        if is_edited:
            data["button"].configure(text=f"✂️ {data['basename']}")

    def preview_audio(self):
        if not self.current_edit_file: return
        audio = self.loaded_audio_cache.get(self.current_edit_file)
        if not audio: return
            
        data = self.files_data[self.current_edit_file]
        start_ms = int(data["start"] * 1000)
        end_ms = int(data["end"] * 1000)
        snippet = audio[start_ms:end_ms]
        
        if len(snippet) < 10:
            return 
            
        snippet = snippet.set_sample_width(2).set_channels(1).set_frame_rate(44100)
        self.log(f"Playing preview ({len(snippet)/1000:.1f}s)...")
        
        try:
            import tempfile
            import winsound
            temp_wav = os.path.join(tempfile.gettempdir(), "edgetx_preview.wav")
            snippet.export(temp_wav, format="wav")
            winsound.PlaySound(temp_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            self.log(f"[ERROR] Playback failed: {e}")

    def sanitize_filename(self, original_name):
        name, ext = os.path.splitext(original_name)
        name = name.lower().replace(" ", "_")
        name = re.sub(r'[^a-z0-9_]', '', name)
        if len(name) > 6:
            name = name[:6]
        return name + ".wav"

    def strip_silence(self, sound, silence_threshold=-50.0, chunk_size=10):
        start_trim = 0
        for i in range(0, len(sound), chunk_size):
            if sound[i:i+chunk_size].dBFS > silence_threshold:
                start_trim = i
                break
        
        end_trim = len(sound)
        for i in range(len(sound), 0, -chunk_size):
            if sound[i-chunk_size:i].dBFS > silence_threshold:
                end_trim = i
                break
        
        start_trim = max(0, start_trim - 50)
        end_trim = min(len(sound), end_trim + 50)
        return sound[start_trim:end_trim]

    def match_target_amplitude(self, sound, target_dBFS=-10.0):
        if sound.dBFS == float('-inf'):
            return sound
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def start_conversion(self):
        if not self.files_data:
            messagebox.showwarning("No Files", "Please select files to convert first.")
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Folder to Save WAV Files")
        if not output_dir:
            return
            
        self.convert_btn.configure(state="disabled", text="Converting...")
        self.log("\n--- Starting conversion ---")
        threading.Thread(target=self.process_files, args=(output_dir,), daemon=True).start()

    def process_files(self, output_dir):
        mode = self.quality_var.get()
        success_count = 0
        
        for filepath, data in self.files_data.items():
            original_filename = data["basename"]
            self.log(f"Processing: {original_filename}")
            
            try:
                if filepath in self.loaded_audio_cache:
                    sound = self.loaded_audio_cache[filepath]
                else:
                    sound = AudioSegment.from_file(filepath)
                
                if data["edited"]:
                    start_ms = int(data["start"] * 1000)
                    end_ms = int(data["end"] * 1000)
                    sound = sound[start_ms:end_ms]
                
                sound = self.strip_silence(sound)
                sound = self.match_target_amplitude(sound, target_dBFS=-10.0)
                
                if mode == "standard":
                    sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
                else:
                    sound = sound.set_frame_rate(44100).set_channels(2).set_sample_width(2)
                
                new_filename = self.sanitize_filename(original_filename)
                output_path = os.path.join(output_dir, new_filename)
                
                if len(sound) > 10000:
                    self.log(f"  [WARN] {new_filename} > 10s. May lag older radios.")
                
                sound.export(output_path, format="wav")
                self.log(f"  [OK] Saved -> {new_filename}")
                success_count += 1
                
            except Exception as e:
                self.log(f"  [ERROR] Failed: {str(e)}")
        
        self.log(f"--- Done! {success_count} files converted ---")
        self.after(0, lambda: self.convert_btn.configure(state="normal", text="Convert All Files"))

if __name__ == "__main__":
    app = EdgeTXConverterApp()
    app.mainloop()
