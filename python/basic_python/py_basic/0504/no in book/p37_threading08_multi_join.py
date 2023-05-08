import threading, time

class sample(threading.Thread):
    def __init__(self, time):
        super(sample, self).__init__() #super를 스면 부모의 클래스가 그대로 자식에게 물려줌(쓰래드 속성을 그대로 물려주고자 할때)
        self.time=time
        self.start()

    def run(self):
        print(self.time, "starts")
        for i in range(0,self.time):
            time.sleep(1)
        print(self.time, "has finished")

t3=sample(3)
t2=sample(2)
t1=sample(1)
t3.join()
print("t3.join() has finished") #조인을 쓰면 끝나는 시간을 순서를 맞추기 위해서 텀을 줌
t2.join()
print("t2.join() has finished")
t1.join()
print("t1.join() has finished")
