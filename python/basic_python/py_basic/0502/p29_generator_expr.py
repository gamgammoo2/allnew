numbers=[1,2,3,4,5]
evens = (2*i for i in numbers)

print(evens)
print(evens.__next__())
print(evens.__next__())
print(sum(evens))

#list generator과 다른점은 이전 내용이 지워지지 않는다는 것

print(numbers)
numbers.reverse()
print(numbers)

evens=(2*i for i in numbers)

print(evens)
print(evens.__next__())
print(evens.__next__())
print(numbers)
print(evens.__next__())

