import speech_recognition as sr
from gtts import gTTS
import os
import playsound

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename='voice.mp3'
    tts.save(filename) # 파일을 만들고,
    playsound.playsound(filename) # 해당 음성파일을 실행(즉, 음성을 말함)
    os.remove(filename) # <---- 이부분이 없으면 퍼미션 에러 발생(아마도 파일을 연 상태에서 추가적인 파일생성 부분에서 에러가 발생하는 것으로 보임)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("지금 말씀하세요: ")
        audio = r.listen(source)
        said = " "

        try:
            said = r.recognize_google(audio, language="ko-KR")
            print("말씀하신 내용입니다 : ", said)
        except Exception as e:
            print("Exception: " + str(e))
    
    return said

#############################
# 0.안내 방송(음성)
#############################
speak("안녕하세요. 2초 후에 '지금 말씀하세요: ' 라는 문장이 나온 후 말 하시면 텍스트로 저장됩니다.") 

#############################
# 1.음성입력
#############################
text=get_audio()


#############################
# 5.파일저장
#############################
with open('memo.txt', 'w') as f:
    f.write(str(text)+"\n")
