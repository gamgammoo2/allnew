import prime_func

a=int(input("please input number : "))

if prime_func.prime(a) == 1:
    print('{} is prime number')
elif prime_func.prime(a) == 2:
    print('{} is not prime number')
else :
    print('please check your input')
