import datetime

#만들어진 class를 decorator처럼 쓸 수 있다.(물론 아직 class를 제대로 배우지는 않음)

class DatetimeDecorator:
    def __init__(self, f):
        self.func=f
    def __call__(self,*args, **kwargs):
        print(datetime.datetime.now())
        self.func(*args, **kwargs)
        print(datetime.datetime.now())
class MainCalss:
    @DatetimeDecorator
    def func1(self):
        print("main function1 start")

    @DatetimeDecorator
    def func2(self):
        print("main function1 start")

    @DatetimeDecorator
    def func3(self):
        print("main function1 start")

my=MainCalss()
my.func1()
my.func2()
my.func3()
