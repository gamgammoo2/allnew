import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import time
from datetime import datetime


def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename='voice.mp3'
    tts.save(filename) # 파일을 만들고,
    playsound.playsound(filename) # 해당 음성파일을 실행(즉, 음성을 말함)
    os.remove(filename) # <---- 이부분이 없으면 퍼미션 에러 발생(아마도 파일을 연 상태에서 추가적인 파일생성 부분에서 에러가 발생하는 것으로 보임)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("지금 말씀하세요: ")
        audio = r.listen(source)
        said = " "

        try:
            said = r.recognize_google(audio, language="ko-KR")
            # print("말씀하신 내용입니다 : ", said)
        except Exception as e:
            pass
            # print("Exception: " + str(e))
    
    return said

#############################
# 0.안내 방송(음성)
#############################
if os.path.isfile('memo.txt'):
    os.remove('memo.txt')

speak("안녕하세요. 2초 후에 말씀하시고, 종료시 '굿바이'라고 말씀하시면 됩니다.")






while True:
    #############################
    # 1.음성입력
    #############################
    text=get_audio()

    print(text)



    #############################
    # 2.파일저장
    #############################
    with open('memo.txt', 'a') as f:
        f.write(str(text)+"\n")

    if "굿바이" in text:
        break

    time.sleep(0.1)
