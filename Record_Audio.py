from playsound import playsound
import pyaudio
import wave
from scipy.signal import butter, lfilter, find_peaks, hilbert
from scipy.io import wavfile
import noisereduce as nr
import soundfile as sf

def normalize(data_array):
    data_array2 = []
    max_element = max(abs(data_array))
    for i in range (0, len(data_array)):
        data_array2.append(data_array[i]/max_element)
    return data_array2

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 5
filename = "OS3.wav"
p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames
# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)
# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
print('Finished recording')
# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames
# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)
# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
print('Finished recording')
# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
playsound(filename)

# Read the audio data
fs, data = wavfile.read(filename)
data = data[:, 0]

# Normalize the data
data = normalize(data)
# Preprocess the raw data
# Filter requirements.
order = 10
cutoff = 4000  # desired cutoff frequency of the filter, Hz
y = butter_lowpass_filter(data, cutoff, fs, order)
noise = y[0:20000]
y_reduced_noise = nr.reduce_noise(audio_clip=y, noise_clip=noise, verbose=False)
y_reduced_noise = normalize(y_reduced_noise)

# Write to file
sf.write(filename, y_reduced_noise, fs)
playsound(filename)