def min (a,b):
    if a>b:
        return b
    else:
        return a
a=input("input first number : ")
b=input("input second number : ")

print("{} vs {} : min number = {}".format(a,b,min(a,b)))