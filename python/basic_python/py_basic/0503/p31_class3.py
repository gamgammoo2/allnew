class SmartPhone(object):
    def __init__(self,brand,maker,price):
        self.brand=brand
        self.maker=maker
        self.price=price
    def __str__(self):
        return  f'str : {self.brand} - {self.maker} - {self.price}'

class Galaxy(SmartPhone):
    def __init__(self, brand, maker, price, country):
        self.brand = brand
        self.maker = maker
        self.price = price
        self.country = country
    def __str__(self):
        return f'str : {self.__class__.__name__}' \
            f'this smartphone released from {self.maker}, '\
            f'manufacture in {self.country}, '\
            f'price is {self.price}. '\

iphone = SmartPhone('Iphone', 'Apple', 10000)
print(iphone)
galaxy = Galaxy('Galaxy', 'Samsung', 8000, 'South Korea')
print(galaxy)