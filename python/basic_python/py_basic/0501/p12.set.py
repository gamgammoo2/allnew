#!/usr/bin/env python

even = set([0,2,4,6,8])
print(even)

hello = set("Hello")
print(hello)

s = even | hello
print(s)

p=even & hello
print(p)

even.add(10)
print(even)

hello.remove('e')
print(hello)

s1=set([1,2,3,4,5])
s2 = set([4,5,6,7,8])

#intersection 교집합
print(s1.intersection(s2))
print(s1 & s2)

#union
print(s1.union(s2))
print(s1 | s2)

#defference
print(s1.difference(s2))
print(s2.difference(s1))
print(s1-s2)
print(s2-s1)

s3 = {1,2,3,4,5}

if s1 == s2:
    print("s1, s2 is same...")
else:
    print("s1, s2 is not same...")

if s1 == s3:
    print("s1, s3 is same...")
else:
    print("s1, s3 is not same...")

s4 = {6,7,8,9,10}

if s1.isdisjoint(s2):
    print("s1, s2 no have in common")
else:
    print("s1, s2 have in common")

if s3.isdisjoint(s4):
        print("s3, s4 no have in common")
else:
        print("s3, s4 have in common")

print(s1.issubset(s2))

s5={4,5}

print(s5.issubset(s1))

s = {1,2,3}
print(f'set:{s}')

s.update({'a','b','c'})
print(f'set:{s}')

s.update(['11','12','13'])
print(f'set:{s}')

s.remove('a')
print(f'set:{s}')

#이미 값이 없을때 리무브하면 에러가 남 <-> discard는 에러는 안남
s.remove('b')
print(f'set:{s}')

s.discard('a')
print(f'set :{s}')

s.discard('b')
print(f'set :{s}')

s={'r','d','t','y','m','q'}

#무작위로 pop되고
print(f'set.pop():{s.pop()}')
print(f'set:{s}')

print(f'set.pop():{s.pop()}')
print(f'set:{s}')

print(f'set.pop():{s.pop()}')
print(f'set:{s}')

s.clear()
print(f'set:{s}')

s={'a','b','c'}

if 'a' in s:
    print('exist')
else:
    print('not exist')

if 'z' in s:
    print('exist')
else:
    print('not exist')

print(f'length of set : {len(s)}')