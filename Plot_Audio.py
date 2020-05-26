import pyaudio
import wave
from scipy.io import wavfile
from matplotlib import pyplot as plt

fs, data = wavfile.read("Raw_Audio/R_AG_1.wav")
plt.plot((data[:,0]))
plt.show()