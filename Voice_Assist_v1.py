DEBUG = 0
USE_METHOD = 'Title'

# Import required packages
import Pkg_voiceRecog as myPkg
import socket
import warnings

warnings.filterwarnings("ignore")
import speech_recognition as sr
from playsound import playsound
from ctypes import *

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    return 0


asound = cdll.LoadLibrary('libasound.so')
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

REMOTE_SERVER = "www.google.com"


def is_connected(hostname):
    """
    This function checks whether the computer is connected to the internet
    :param hostname: Hostname of the server
    :return: True if connected, False if not
    """
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        print("Connection Established")
        return True
    except:
        pass
    print("Connection Error! Switched to Offline Mode")
    return False


def check_if_OK(CONNECTION_ESTD):
    """
    This function checks whether you got the step or need to hear it again.
    It records your response and recognizes your voice command
    :param CONNECTION_ESTD: boolean variable telling whether to use the offline/online mode
    :return: True is user understood the step false if not
    """
    DETECTED = False
    while (DETECTED == False):
        myPkg.record_voice(3)
        if (CONNECTION_ESTB):
            r = sr.Recognizer()
            with sr.AudioFile("temp.wav") as source:
                audio = r.record(source)  # read the entire audio file
            # recognize speech using Google Speech Recognition
            try:
                usr_ip = r.recognize_google(audio)
                usr_ip = usr_ip.lower()
                print("You said " + usr_ip)
                if (
                        "achcha" in usr_ip or "ok" in usr_ip or "next" in usr_ip or "text" in usr_ip or "agla" in usr_ip or "aage" in usr_ip):
                    DETECTED = True
                    return True
                elif ("wapas" in usr_ip or "fir" in usr_ip or "repeat" in usr_ip or "kya" in usr_ip):
                    DETECTED = True
                    return False
            except sr.UnknownValueError:
                print("Can't hear you")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            usr_ip = myPkg.recogPhrase('temp.wav', 'Instruction', DEBUG)
            if (usr_ip == 'AG'):
                DETECTED = True
                return True
            elif (usr_ip == 'FSB'):
                DETECTED = True
                return False
            else:
                pass


def train_for_faasos(CONNECTION_ESTB):
    """
    This function is called when the user needs training for Faasos
    :param CONNECTION_ESTB: boolean variable telling whether to use the offline/online mode
    :return:
    """
    STEP1_OK = False
    STEP2_OK = False
    STEP3_OK = False
    STEP4_OK = False

    while (STEP1_OK == False):
        mytext = 'Pehla step, maidaa aur roti lijiye'
        print(mytext)
        print("Agla Step / Fir se Bataiye")
        file = "Recorded_Voices_Female/Faasos/Step_1.wav"
        playsound(file)
        STEP1_OK = check_if_OK(CONNECTION_ESTB)
    while (STEP2_OK == False):
        mytext = 'Filling daaliye'
        print(mytext)
        print("Agla Step / Fir se Bataiye")
        file = "Recorded_Voices_Female/Faasos/Step_2.wav"
        playsound(file)
        STEP2_OK = check_if_OK(CONNECTION_ESTB)
    while (STEP3_OK == False):
        mytext = 'Paper me wrap kijiye'
        print(mytext)
        print("Agla Step / Fir se Bataiye")
        file = "Recorded_Voices_Female/Faasos/Step_3.wav"
        playsound(file)
        STEP3_OK = check_if_OK(CONNECTION_ESTB)
    while (STEP4_OK == False):
        mytext = 'Box me daaliye'
        print(mytext)
        print("Agla Step / Fir se Bataiye")
        file = "Recorded_Voices_Female/Faasos/Step_4.wav"
        playsound(file)
        STEP4_OK = check_if_OK(CONNECTION_ESTB)
    mytext = 'Faasos tayaar hai!'
    print(mytext)
    print("Thank You!")
    file = "Recorded_Voices_Female/Faasos/END.wav"
    playsound(file)
    return 0


def train_for_behrouz(CONNECTION_ESTD):
    """
    This function is called when the user needs training for Behrouz Biryani
    :param CONNECTION_ESTB: boolean variable telling whether to use the offline/online mode
    :return:
    """

    print("This recipe is yet to be developed")
    print("See you later :)")
    return 0


def train_for_ovenstory(CONNECTION_ESTD):
    """
    This function is called when the user needs training for Oven Story Pizza
    :param CONNECTION_ESTB: boolean variable telling whether to use the offline/online mode
    :return:
    """

    print("This recipe is yet to be developed")
    print("See you later :)")
    return 0


# Check whether server is connected
print("Establishing Connection to Server...")
CONNECTION_ESTB = is_connected(REMOTE_SERVER)

# Initialize the microphone
print("Initializing microphone")
myPkg.record_voice(3)
print("Microphone initialized!")

# Play the intro message
print("Namaskar, konsa training karna hai?")
file = "Recorded_Voices_Female/Intro.wav"
playsound(file)

if (CONNECTION_ESTB == True):
    # Online Mode
    DETECTED = False
    while (DETECTED == False):
        myPkg.record_voice(3)
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)  # read the entire audio file
        # recognize speech using Google Speech Recognition
        try:
            usr_ip = r.recognize_google(audio)
            print("You said " + usr_ip)
            if ("faasos" in usr_ip or "Asus" in usr_ip or "shoes" in usr_ip or "propose" in usr_ip or "passes" in usr_ip):
                DETECTED = True
                train_for_faasos(CONNECTION_ESTB)
            if ("behrouz" in usr_ip or "biryani" in usr_ip or "rice" in usr_ip):
                DETECTED = True
                train_for_behrouz()
            if ("oven" in usr_ip or "story" in usr_ip or "ovenstory" in usr_ip or "pizza" in usr_ip):
                DETECTED = True
                train_for_ovenstory()
        except sr.UnknownValueError:
            print("We could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
else:
    # Offline mode
    print("Available Recipes: (Say exactly same words)")
    print("Faasos")
    print("Behrouz Biryani")
    print("Oven Story Pizza")
    DETECTED = False
    while (DETECTED == False):
        myPkg.record_voice(3)
        usr_ip = myPkg.recogPhrase('temp.wav', USE_METHOD, DEBUG)
        if (usr_ip == 'FA'):
            DETECTED = True
            train_for_faasos(CONNECTION_ESTB)
        elif (usr_ip == 'BZ'):
            DETECTED = True
            train_for_behrouz(CONNECTION_ESTB)
        elif (usr_ip == 'OS'):
            DETECTED = True
            train_for_ovenstory(CONNECTION_ESTB)
        else:
            pass
