import threading, queue, time

work=queue.Queue()
def generator(start, end):
    for _ in range(start, end):
        work.put(_)

def display():
    while work.empty() is False:
        data = work.get()
        print(
            'data is ' + str(data)
        )
        time.sleep(1)
        work.task_done()

threading.Thread(target=generator, args =(1,10)).start()
threading.Thread(target=display).start()
work.join()

#work.task_done() 과 work.join()은 세트다. 그동안 다른것들이 들어오지 못하게 했다가 (work가 empty인 순간까지 ) 끝나면 lock을 풀어줌.