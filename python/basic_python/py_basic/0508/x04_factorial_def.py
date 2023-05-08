def factorial(x):
    if x ==0:
        return 1
    else:
        return x * factorial(x-1)

input = int(input("input the number : "))
print(f'{input} factorial = {factorial(input)}')