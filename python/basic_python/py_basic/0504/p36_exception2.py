a="Hello"
b=1

try:
    c=a+b #문자열과 숫자를 더했기때문에 발생하는 에러
    print(c)
except :
    print('the error is occurred')
finally:
    print(a)

