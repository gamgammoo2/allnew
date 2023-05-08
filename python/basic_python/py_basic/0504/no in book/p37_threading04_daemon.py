#deamon Thread
import threading, requests, time

"""
Thread class 속성 중 daemon 속성은 sub thread가 daemon thread인지 여부를 지정. 
daemon thread는 background thread로 main thread가 종료되면 즉시 종료됨.
반면 daemon thread가 아닌 thread는 Main Thread와 관계없이 자신의 작업이 끝날때까지 계속 실행되는 특징이 있음."""

def getHtml(url):
    resp=requests.get(url)
    time.sleep(2)
    print(url, len(resp.text), 'chars')

t = threading.Thread(target = getHtml, args = ('http://google.com',))
t.daemon = True
t.start()

#굳이 보고싶다.
#while True:
    #for _ in range(5)
        #time.sleep(1)
    #print('###End###')
    #끝내고싶으면 break
print('### End ###') #메인스레드임. 이게 끝날때 같이 끝내버림

#무한루프로 돌리는 이유 예시: 우리가 정보를 5분에 1번씩 받아와서 몽고디비에 업데이트 해버리고 싶을 때 라거나... 백그라운드 대기 하는 겨...
#스레드의 실행순서는 보장할 수 없다.