a=int(input("input 1st number to get greatest common divisor : "))
b=int(input("input 2nd number to get greatest common divisor : "))

class calc(object):
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def gcd(self):
        print("gcd",(self.a,self.b))
        while self.b!=0:
            r=self.a%self.b
            self.a=b
            self.b=r
            print("gcd,(a,b)")
        return self.a
R=calc()
print(f'gcd({a},{b}) of {a},{b} : {calc.gcd(a,b)}')
