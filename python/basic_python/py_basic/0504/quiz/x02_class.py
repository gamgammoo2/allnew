import random

class findMax(object): #오브잭트에는 암것도 안써야함 (내가 상속할 객체만 써야함)
    def __init__(self,data): #max가 아니라 data가 들어가야했음./ 아래에도 self.data로 바꿔야함....
        self.data=data
    def max(self):
        max=self.data[0]
        for i in range(1,len(self.data)):
            if self.data[i]>max:
                max=self.data[i]
        return max

data=random.sample(range(1,101),10)
print(data)

data1=findMax(data)
print(f'Max value is : {data1.max()}')