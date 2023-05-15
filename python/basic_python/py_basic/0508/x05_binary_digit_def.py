import random

d=random.randrange(4,17)
print(f'binary of {d}')

# 복잡해도 양해 발암...
def binary_digit(d):
    binary=[]
    while (d*2)//2>0:
        r=d%2
        binary.append(r)
        d=d//2
    return(list(reversed(binary)))

print(binary_digit(d))