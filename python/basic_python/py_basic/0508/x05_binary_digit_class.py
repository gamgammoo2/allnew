# import random
#
# class Binary_digits(object):
#     def __init__(self,d):
#         self.d=d
#     def covert(self):
#         binary = []
#         while (self.d * 2) // 2 > 0:
#             r = self.d % 2
#             binary.append(r)
#             self.d = self.d // 2
#         return (list(reversed(binary)))
#
# d=random.randrange(4,17)
# result=Binary_digits(d)
# print(f'Binary of {d} = {result.covert()}')

import random

def convertbinary(x):
    temp = []
    while True:
        remain = x % 2
        x = x // 2
        temp.append(remain)

        if x < 2:
            temp.append(x)
            break
    temp.reverse()
    return temp

x = random.randint(4, 16)
binary_x = convertbinary(x)

print(f'{x} = {binary_x}')

