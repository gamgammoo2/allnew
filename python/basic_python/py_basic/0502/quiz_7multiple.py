import p25_timer

timer= p25_timer.counter2()

for i in range(1,100):
    if i % 7 ==0:
        print(timer())