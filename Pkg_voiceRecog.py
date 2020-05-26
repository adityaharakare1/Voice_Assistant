# Import required packages
from scipy.io import wavfile
import noisereduce as nr
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter, find_peaks, hilbert
from playsound import playsound
import pyaudio
import wave
from ctypes import *

# Suppress any warning
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    return 0


asound = cdll.LoadLibrary('libasound.so')
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)


def record_voice(time):
    '''
    This functions records the voice from the microphone
    :param time: time for which microphone records the voice
    :return: Nil
    '''
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = time
    filename = "temp.wav"
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

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return 0


def normalize(data_array):
    '''
    This functions normalizes the input array
    :param data_array: input array
    :return: normalized array
    '''
    data_array2 = []
    max_element = max(abs(data_array))
    for i in range(0, len(data_array)):
        data_array2.append(data_array[i] / max_element)
    return data_array2


def find_abs_array(array):
    """
    This function returns the absolute value of each element of an array
    :param array:
    :return:
    """
    for i in range(0, len(array)):
        array[i] = abs(array[i])
    return array


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    Returns the low pass filtered data
    :param data: input data
    :param cutoff: cutoff frequency
    :param fs: sampling frequency
    :param order: Order of the filter
    :return: output array
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def high_pass_filter(data, fs, cutoff_freq):
    """
    This function applies the high pass filter to the input data
    :param data: Input array
    :param fs: Sampling frequency
    :param cutoff_freq: cutoff frequency
    :return: High pass filtered data
    """
    sos = signal.butter(10, cutoff_freq, 'hp', fs=fs, output='sos')
    filtered = signal.sosfilt(sos, data)
    return filtered


def smooth(x, window_len=11, window='hanning'):
    """
    Smooths the data curve
    :param x: input data
    :param window_len: amount of smoothing required
    :param window: type of filter
    :return: smoothed data
    """
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


def postprocess(data_array):
    """
    Handles the processing before matching
    :param data_array: input data
    :return: processed data
    """
    # analytic_signal = hilbert(data_array)
    analytic_signal = np.array(find_abs_array(data_array))
    # amplitude_envelope = np.abs(analytic_signal)
    # smooth_envelope = smooth(amplitude_envelope, window_len=100)
    nor_smooth_envelope = normalize(analytic_signal)
    return nor_smooth_envelope


def find_corr(path1, path2, DEBUG):
    """
    Finds the correlation between two audio data files
    :param path1: Location of the clean recorded audio
    :param path2: Location of the raw input audio
    :param DEBUG: Plots and outputs debug data on terminal if val=1
    :return: Correlation between the two audio files
    """
    if DEBUG == 1:
        DEBUG = True
    # Read the audio data
    fs, data = wavfile.read(path1)
    fs_raw, data_raw = wavfile.read(path2)
    data_raw = data_raw[:, 0]

    # No voice detected check-1
    if max(data_raw) < 10000:
        return -1000

    # Normalize the data
    data_raw = normalize(data_raw)
    data = normalize(data)
    if DEBUG:
        plt.plot(data_raw)
        plt.show()
        plt.plot(data)
        plt.show()

    # Preprocess the raw data
    # High Pass Filter
    data_raw = high_pass_filter(data_raw, fs_raw, 85)
    plt.plot(data_raw)
    # Hamming Filter
    data_raw = data_raw * np.hamming(len(data_raw))
    plt.plot(data_raw)
    # Lowpass Filter
    order = 10
    cutoff = 4000  # desired cutoff frequency of the filter, Hz
    y = butter_lowpass_filter(data_raw, cutoff, fs_raw, order)
    noise = y[0:20000]
    # Noise Reduction
    y_reduced_noise = nr.reduce_noise(audio_clip=y, noise_clip=noise, verbose=False)
    y_reduced_noise = normalize(y_reduced_noise)
    plt.plot(y_reduced_noise)
    if DEBUG == True:
        plt.show()

    # Find the bin where the voice is present
    # This uses the concept of sliding windows
    bin1 = 5000
    bin2 = 5000
    bin_ratio1 = []
    bin_ratio2 = []
    abs_y_reduced_noise = find_abs_array(y_reduced_noise.copy())
    bin1_val = sum(abs_y_reduced_noise[0:bin1 - 1])
    bin2_val = sum(abs_y_reduced_noise[bin1: bin1 + bin2 - 1])
    for i in range(0, len(y_reduced_noise) - bin1 - bin2):
        bin_ratio1.append((bin2_val + .5) / (bin1_val + .5))
        bin_ratio2.append((bin1_val + .5) / (bin2_val + .5))
        bin1_val = bin1_val + abs_y_reduced_noise[i + bin1] - abs_y_reduced_noise[i]
        bin2_val = bin2_val + abs_y_reduced_noise[i + bin1 + bin2] - abs_y_reduced_noise[i + bin1]

    # make the peaks of bin_ratios of the same height
    if max(bin_ratio1) - max(bin_ratio2) > 0:
        mul_fac = max(bin_ratio1) / max(bin_ratio2)
        for i in range(0, len(bin_ratio2)):
            bin_ratio2[i] = (bin_ratio2[i]) * mul_fac
    else:
        mul_fac = max(bin_ratio2) / max(bin_ratio1)
        for i in range(0, len(bin_ratio1)):
            bin_ratio1[i] = (bin_ratio1[i]) * mul_fac

    if DEBUG:
        plt.plot(bin_ratio1)
        plt.plot(bin_ratio2)
        plt.show()

    peaks1 = find_peaks(bin_ratio1, prominence=8)
    peaks2 = find_peaks(bin_ratio2, prominence=8)
    n_peaks1 = len(peaks1[0])
    n_peaks2 = len(peaks2[0])

    # If no peaks are detected then break
    if n_peaks1 == 0 or n_peaks2 == 0:
        return -1000

    # Assign voice start and end values
    voice_start = peaks1[0][0] + bin1
    voice_end = peaks2[0][n_peaks2 - 1] + bin1
    # print(voice_start, voice_end)

    # Correct for noise before voice
    voice_peak = y_reduced_noise.index(max(y_reduced_noise))
    index1 = 0
    while voice_peak - voice_start > 40000:
        if n_peaks1 == index1 + 1:
            break
        voice_start = peaks1[0][index1 + 1] + bin1
        index1 = index1 + 1
        if DEBUG:
            print("Bad Noise Detected before start")
    index2 = 0
    while voice_end - voice_peak > 40000:
        if n_peaks2 - 2 - index2 == -1:
            break
        voice_end = peaks2[0][n_peaks2 - 2 - index2] + bin1
        index2 = index2 + 1
        if DEBUG:
            print("Bad Noise Detected after end")

    # Correct for noise just before voice
    max_val1 = max(y_reduced_noise[voice_start:voice_start + 10000])
    while max_val1 < 0.2:
        if index1 + 1 == n_peaks1:
            break
        if DEBUG:
            print("Noise Detected just before voice")
        voice_start = peaks1[0][index1 + 1] + bin1
        index1 = index1 + 1
        max_val1 = max(y_reduced_noise[voice_start:voice_start + 10000])

    # Correct for noise just after voice
    max_val2 = max(y_reduced_noise[voice_end - 10000:voice_end])
    while max_val2 < 0.2:
        if n_peaks2 - 2 - index2 == -1:
            break
        if DEBUG:
            print("Noise Detected just after voice")
        voice_end = peaks2[0][n_peaks2 - 2 - index2] + bin1
        index2 = index2 + 1
        max_val2 = max(y_reduced_noise[voice_end - 10000:voice_end])

    inp_phrase = y_reduced_noise[voice_start:voice_end]

    # Resample the data to make the number of sample points same
    if len(inp_phrase) > len(data):
        inp_phrase = signal.resample(inp_phrase, len(data))
    else:
        data = signal.resample(data, len(inp_phrase))

    if DEBUG:
        plt.plot(inp_phrase)
        plt.plot(data)
        plt.show()

    # Postprocess the data and find the correlation
    inp_phrase = postprocess(inp_phrase)
    data = postprocess(data)
    corr = 100 * np.corrcoef(data, inp_phrase)[0, 1]
    # print(corr)
    return corr


def recogPhrase(filename, position, DEBUG):
    """
    Recognizes the voice phrase from the audio file
    :param filename: Input file location
    :param position: Specify whether it is the title or an instruction
    :param DEBUG: Outputs the plot and debug data if val=1
    :return: The code of the phrase
    AG: Agla Step
    FSB: Fir se Bataiye
    """
    if position == "Instruction":
        corr1 = find_corr('Recorded/AG.wav', filename, DEBUG)
        corr2 = find_corr('Recorded/FSB2.wav', filename, DEBUG)
        if corr1 == -1000 or corr2 == -1000:
            print("Sorry we couldn't hear you!")
            return -1
        if corr1 > corr2:
            print("You said 'Agla Step'")
            return 'AG'
        else:
            print("You said Fir se bataiye")
            return 'FSB'
    elif position == "Title":
        corr1 = find_corr('Recorded/FA2.wav', filename, DEBUG)
        corr2 = find_corr('Recorded/BZ3.wav', filename, DEBUG)
        corr3 = find_corr('Recorded/OS3.wav', filename, DEBUG)
        if corr1 == -1000 or corr2 == -1000 or corr3 == -1000:
            print("Sorry we couldn't hear you!")
            return -1
        if corr1 > corr2 and corr1 > corr3:
            print("You said 'Faasos'")
            return 'FA'
        elif corr2 > corr1 and corr2 > corr3:
            print("You said 'Behrouz Biryani'")
            return 'BZ'
        else:
            print("You said 'Oven Story Pizza'")
            return 'OS'
    elif position == 'Title_AL':
        print("1: Faasos")
        print("2: Behrouz")
        print("3: Oven Story")
        corr1 = find_corr('Recorded/ONE.wav', filename, DEBUG)
        corr2 = find_corr('Recorded/TWO.wav', filename, DEBUG)
        corr3 = find_corr('Recorded/THREE.wav', filename, DEBUG)
        if corr1 == -1000 or corr2 == -1000 or corr3 == -1000:
            print("Sorry we couldn't hear you!")
            return -1
        if corr1 > corr2 and corr1 > corr3:
            print("You said 'One'")
            return 'FA'
        elif corr2 > corr1 and corr2 > corr3:
            print("You said 'Two'")
            return 'BZ'
        else:
            print("You said 'Three'")
            return 'OS'
    else:
        return "Position error"


# Reset to default error handler
asound.snd_lib_error_set_handler(None)
# Re-initialize
