import threading, time

data =0
lock = threading.Lock()

def generator(start, end):
    global data
    for _ in range(start, end):
        lock.acquire()
        buf = data
        time.sleep(0.01)
        data = buf + 1
        lock.release()

t1=threading.Thread(target=generator, args =(1,10))
t2=threading.Thread(target=generator, args=(1,10))

t1.start()
t2.start()

t1.join()
t2.join() #join은 done이 없으면(쓰레드가 종료되기까지 기다리는 애인데) ->이 로직은 언제 done 되는지 파악하기 힘들다.

print(data)