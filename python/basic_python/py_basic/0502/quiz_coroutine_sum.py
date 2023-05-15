def handler():
    while True:
        v1,v2 = (yield)
        print(f"{v1} + {v2} = {v1+v2}")

result=handler()
result.__next__()
result.send([5,4])
result.send([3,6])
#send 보내면 while문에서 print까지 한바퀴 돌고 while문 도는것 전 까지 가있음
#처음에 while 돌리기 위해서 next를 사용한거임 (왜냐면 이전에 send로 보낸 게 없으니까)


