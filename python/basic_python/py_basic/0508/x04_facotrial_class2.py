
class Factorial(object):
    def __init__(self,x):
        self.x=x
    def factorial(self):
        n=1
        for i in range(1,self.x + 1):
            n=n*i
        return n
        # if self.x==0:
        #     return 1
        # else:
        #     return self.x * Factorial.factorial(self.x-1)

x = int(input("input the number : "))

result = Factorial(x)

print(f'{x} factorial = {result.factorial()}')