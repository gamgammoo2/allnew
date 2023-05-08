#yield기반 프로그램 send를 보내면 coroutin 안에 yield가 받음 .(앞서 배운 제너레이터에 더해서 파라미터까지 주고싶음 ->이걸 받는게 yield)
def handler():
    print("Initialize Handler")
    while True:
        value = (yield)
        print("receive %s " % value)

listener = handler()
listener.__next__()
listener.send(1)
listener.send("message")