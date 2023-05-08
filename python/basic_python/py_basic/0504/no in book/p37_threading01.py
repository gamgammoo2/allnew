#thread -> 아이티 에서는 묶음 처리 : 여러개가 동시에 처리되는 것(페이지가 될수도 있고 등등... 뭐라는지 못들음)
import threading
def sum(low, high):
    total = 0
    for i in range(low, high):
        total += i
    print('Sub thread : ', total)

t = threading.Thread(target = sum, args = (1,100000))
t.start()

print('Main Thread')

#스레드의 실행순서는 보장할 수 없다.