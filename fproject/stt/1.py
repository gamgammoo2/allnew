import speech_recognition as sr

# 음성 녹음
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak anything:")
    audio = r.listen(source)

# 음성 인식
try:
    text = r.recognize_google(audio, language='ko-KR')
    print("You said: {}".format(text))
except:
    print("Sorry, could not recognize your voice.")
