
def share (a,b):
    x=a/b
    return x

def remainder (a,b):
    y=a%b
    return y

a=int(input("input first number : "))
b=int(input("input second number : "))

print("input number : {} / {}".format(a,b))
print("Quotient : {}".format(share(a,b)))
print("Remainder : {}".format(remainder(a,b)))