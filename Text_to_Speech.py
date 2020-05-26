from gtts import gTTS
mytext = 'Faasos tayaar hai!'
language = 'hi'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("Recorded_Voices_Female/Faasos/END.wav")

