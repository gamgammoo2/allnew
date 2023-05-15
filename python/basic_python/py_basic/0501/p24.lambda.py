i=input("input first number : ")
j = input("input second number : ")

a=lambda i, j : i+j
print('{} + {} = {}'.format(i,j,a(int(i),int(j))))