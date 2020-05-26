import Pkg_voiceRecog as myPkg

# Initialize the microphone
print("Microphone Initializing (Please Wait)")
myPkg.record_voice(3)
print("Initialized")

while True:
    usr_input = 'y'
    if(usr_input.lower()=='n'):
        break
    else:
        print("Recording Now!")
        myPkg.record_voice(5)
        print("Recording Over")
        # playsound("temp.wav")
        usr_phrase = myPkg.recogPhrase('temp.wav', 'Instruction', 0)
        usr_input = input("Again? (Y/N) ")
