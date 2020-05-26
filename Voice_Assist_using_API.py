import warnings
warnings.filterwarnings("ignore")
import pyaudio
import wave
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
from ctypes import *
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  return 0
asound = cdll.LoadLibrary('libasound.so')
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

DETECTED = False
def check_if_OK():
    DETECTED = False
    while (DETECTED == False):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        seconds = 3
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
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)  # read the entire audio file
        # recognize speech using Google Speech Recognition
        try:
            usr_ip = r.recognize_google(audio)
            usr_ip=usr_ip.lower()
            print("You said " + usr_ip)
            if ("achcha" in usr_ip or "ok" in usr_ip or "next" in usr_ip or "text" in usr_ip or "agla" in usr_ip or "aage" in usr_ip):
                DETECTED = True
                return True
            elif ("wapas" in usr_ip or "fir" in usr_ip or "repeat" in usr_ip or "kya" in usr_ip):
                DETECTED = True
                return False
        except sr.UnknownValueError:
            print("Can't hear you")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def train_for_faasos():
    STEP1_OK = False
    STEP2_OK = False
    STEP3_OK = False
    STEP4_OK = False

    while(STEP1_OK == False):
        mytext = 'Pehla step, maida aur roti lijiye'
        print(mytext)
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("speech_op.wav")
        file = "speech_op.wav"
        playsound(file)
        STEP1_OK = check_if_OK()
    while(STEP2_OK == False):
        mytext = 'Filling daaliye'
        print(mytext)
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("speech_op.wav")
        file = "speech_op.wav"
        playsound(file)
        STEP2_OK = check_if_OK()
    while(STEP3_OK == False):
        mytext = 'Paper me wrap kijiye'
        print(mytext)
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("speech_op.wav")
        file = "speech_op.wav"
        playsound(file)
        STEP3_OK = check_if_OK()
    while (STEP4_OK == False):
        mytext = 'Box me daaliye'
        print(mytext)
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("speech_op.wav")
        file = "speech_op.wav"
        playsound(file)
        STEP4_OK = check_if_OK()
    mytext = 'Faasos tayaar hai!'
    print(mytext)
    print("Thank You!")
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("speech_op.wav")
    file = "speech_op.wav"
    playsound(file)
    return 0

def train_for_behrouz():
    return 0
def train_for_ovenstory():
    return 0

file = "Recorded_Voices_Female/Intro.wav"
playsound(file)

while(DETECTED == False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Which recipe do you want to learn? ")
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
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
    print('Finished recording')
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        usr_ip = r.recognize_google(audio)
        print("You said " + usr_ip)
        if (usr_ip == "faasos" or usr_ip == "Asus" or usr_ip == "shoes" or usr_ip == "propose"or usr_ip == "passes"):
            DETECTED = True
            train_for_faasos()
        if (usr_ip == "behrouz"):
            DETECTED = True
            train_for_behrouz()
        if (usr_ip == "oven" or usr_ip == "story" or usr_ip == "ovenstory" ):
            DETECTED = True
            train_for_ovenstory()
    except sr.UnknownValueError:
        print("We could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
DETECTED = False

# Reset to default error handler
asound.snd_lib_error_set_handler(None)
# Re-initialize
DETECTED = False