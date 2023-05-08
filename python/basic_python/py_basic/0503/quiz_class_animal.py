class animal(object):
    def __init__(self,name):
        self.name=name
    def move(self):
        print("move~")
    def speak(self):
        pass
class Dog(animal):
    def speak(self):
        print("woof")
class Duck(animal):
    def speak(self):
        print("quack")
