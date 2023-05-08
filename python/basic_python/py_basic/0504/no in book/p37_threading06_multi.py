import threading
def example():
    for _ in range(1,10):
        print(_)

threading.Thread(target=example).start()
threading.Thread(target=example).start()

#지 멋대로 나옴. 이게 필요할 때가 있을 겨 ... 극단적인 예시지만은서도