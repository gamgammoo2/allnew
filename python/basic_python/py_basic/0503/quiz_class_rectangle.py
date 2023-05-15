class Rectangle(object):
    count=0

    def __init__(self,wid,hei):
        self.wid=wid
        self.hei=hei
        Rectangle.count+=1

    def printCount(cls):
        print(cls.count)

    def isSquare(width,height):
        return width==height
    def calcArea(self):
        return self.wid * self.hei

    def __add__(self,rect):
        return Rectangle(self.wid+rect.wid, self.hei+rect.hei)