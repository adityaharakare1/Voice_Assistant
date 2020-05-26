from scipy import signal
from scipy.signal import butter, lfilter, find_peaks, hilbert
import wave
from scipy.io import wavfile
from matplotlib import pyplot as plt

fs, data = wavfile.read("Raw_Audio/R_AG_1.wav")
data = data[:, 0]
plt.plot(data)

sos = signal.butter(10, 85, 'hp', fs=fs, output='sos')
filtered = signal.sosfilt(sos, data)
plt.plot(filtered)
plt.show()