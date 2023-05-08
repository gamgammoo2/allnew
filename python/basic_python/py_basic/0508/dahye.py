import random

class BinaryConverter:
    def __init__(self, x):
        self.x = x

    def convert(self):
        temp = []
        while True:
            remain = self.x % 2
            self.x = self.x // 2
            temp.append(remain)

            if self.x <= 1:
                temp.append(self.x)
                return temp[::-1]
                break

x=random.randint(4,17)
t=BinaryConverter(x)
print(f'{x}={t.convert()}')
