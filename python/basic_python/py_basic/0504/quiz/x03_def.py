a=int(input("input 1st number to get greatest common divisor : "))
b=int(input("input 2nd number to get greatest common divisor : "))
def gcd(a, b):
    print("gcd", (a, b))
    while b != 0:
        r = a % b
        a = b
        b = r
        print("gcd", (a, b))
    return a

print(f'gcd({a}, {b}) of {a}, {b} : {gcd(a, b)}')



