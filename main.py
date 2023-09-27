import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import soundfile as sf
import pyloudnorm as pyln
from pydub import AudioSegment
import numpy as np
from tkinter import ttk 
from PIL import Image, ImageTk

standards_in_db = {'tv': -24, 'streaming': -14, 'podcast': -19}
standards_in_amplitude = {'tv': 0.0631, 'streaming': 0.1995, 'podcast': 0.1122}

class AudioNormalizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Jayden\'s Audio Normalizer')
        self.master.geometry('300x550')  # Updated dimensions to fit image
        self.master.configure(bg='lightgrey')

        frame = ttk.Frame(master, padding='10')
        frame.pack(fill=tk.BOTH, expand=tk.YES)

        # Load and resize image using Pillow
        img = Image.open("AlbumArt.jpeg")
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(img)

        # Display image
        ttk.Label(frame, image=self.logo).grid(row=0, column=1, rowspan=5)


        self.filename = None
        self.data = None
        self.sample_rate = None
        self.loudness = None

        frame = ttk.Frame(master, padding='10')
        frame.pack(fill=tk.BOTH, expand=tk.YES)

        ttk.Button(frame, text="Open File", command=self.load_file).grid(row=0, column=0, pady=5)
        ttk.Button(frame, text="Normalize Audio", command=self.normalize_audio).grid(row=1, column=0, pady=5)
        ttk.Button(frame, text="Show Data", command=self.show_data).grid(row=2, column=0, pady=5)
        ttk.Button(frame, text="Show Graph", command=self.show_graph).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Quit", command=master.quit).grid(row=4, column=0, pady=5)

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if self.filename:
            self.data, self.sample_rate = sf.read(self.filename)
            self.loudness = self.get_loudness(self.data, self.sample_rate)

    @staticmethod
    def get_loudness(data, sample_rate):
        meter = pyln.Meter(sample_rate)
        return meter.integrated_loudness(data)

    def normalize_audio(self):
        if self.data is not None:
            threshold = self.choose_limit('db')
            if threshold is not None:
                sound = AudioSegment.from_file(self.filename, "wav")
                self.set_loudness(sound, threshold)

    def show_data(self):
        if self.loudness is not None:
            messagebox.showinfo("Audio Data", f"Loudness: {round(self.loudness, 1)} LUFS\nSample rate: {self.sample_rate} Hz")

    def show_graph(self):
        if self.data is not None:
            threshold = self.choose_limit('amplitude')
            if threshold is not None:
                self.graph_audio(self.data, self.sample_rate, threshold)

    def choose_limit(self, unit='db'):
        options = ', '.join(standards_in_db.keys() if unit == 'db' else standards_in_amplitude.keys())
        choice = simpledialog.askstring("Choose Limit", f"Choose a limit for {unit.upper()} (Options: {options}):")
        standards = standards_in_db if unit == 'db' else standards_in_amplitude
        return standards.get(choice.lower())

    def set_loudness(self, sound, threshold):
        difference_in_loudness = threshold - sound.dBFS
        normalized_sound = sound.apply_gain(difference_in_loudness)
        normalized_sound.export(self.filename, format="wav")

    def graph_audio(self, data, sample_rate, threshold):
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Audio Graph")

        fig = Figure(figsize=(12, 4))
        ax = fig.add_subplot(111)

        seconds = np.linspace(0, len(data) / sample_rate, num=len(data))

        ax.plot(seconds, data, color='b')
        ax.axhline(y=threshold, color='r', linestyle='--')
        ax.set_title('Audio File')
        ax.set_ylabel('Amplitude')
        ax.set_xlabel('Time (s)')

        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioNormalizerApp(root)
    root.mainloop()
