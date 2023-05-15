
class Factorial(object):
    def __init__(self,x):
        self.x=x
    def factorial(self):
        if self.x==0:
            return 1
        n=self.x
        self.x-=1
        return n*self.factorial()
        # else:
        #     return self.x * Factorial.factorial(self.x-1)

x = int(input("input the number : "))

result = Factorial(x)

print(f'{x} factorial = {result.factorial()}')