import quiz_calc_class
a= int(input('Input first number : '))
b=int(input('Input second number : '))

my = quiz_calc_class.calc(a, b)

print(f'{a} + {b} = {my.add()}')
print(f'{a} - {b} = {my.sub()}')
