### Jayden's Audio Normalizer

An intuitive desktop application built with Tkinter that provides functionalities to normalize audio levels and visualize audio data. It uses libraries like soundfile, pyloudnorm, pydub, and matplotlib to process and analyze WAV audio files.

#### Features:
1. **Load Audio**: Load `.wav` audio files into the application.
2. **Normalize Audio**: Normalize the audio file based on a chosen broadcasting standard (TV, Streaming, Podcast).
3. **Show Data**: Displays integrated loudness and sample rate of the loaded audio file.
4. **Visualize Audio**: Plot the audio signal with time and mark the chosen amplitude threshold.

#### Dependencies:
- `tkinter` for GUI.
- `soundfile` to read audio data.
- `pyloudnorm` to compute integrated loudness.
- `pydub` to normalize audio.
- `matplotlib` to plot audio data.
- `PIL` (Pillow) to manage and display images in the application.

#### Usage:
Simply run the script and navigate through the application to load an audio file, normalize it, and visualize its data.
