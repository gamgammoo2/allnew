me={"name":"gam","age": 26,"gender":"female"}
print(me)

myname = me["name"]
print(myname)

me["age"] =25
print(me)

dict={}
print(dict)

#숫자키에 숫자값
me[10] =10
print(me)

#문자키에 숫자값
me['10'] =10
print(me)

me['job']='teacher'
print(me)

#문자키에 리스트
me['list']=[1,2,3,4,5]
print(me)

#튜플은 변하지 않는 값이라, 리스트의 값이 변하는것이 아니라, 새로 추가된 것.
me[(1,2)] ="this is value"
print(me)

me[(1,2)]='i can do'

me[(1,2)]=(1,2,3,4,5)

me[(1,2)]=(3,5)

me[10]=5

me['10']=5

me[3]=(3, 'aa', 5)
print(me)

print('===========')
print(f'me[list] : {me["list"]}')
print(f'me[(1,2)] : {me[(1,2)]}')
print(f'me[3] : {me[3]}')

print(f'me[(1,2)] : {me[(1,2)]}')
me[(1,2)] = "this is real value"
print(f'me[1,2] : {me[(1,2)]}')

dic = {'a': 1234, 'b': 'blog', 'c':3333}

if 'b' in dic:
    print("b is exist")
else:
    print("b is not exist")

if 'e' in dic:
    print("e is exist")
else:
    print("e is not exist")

print(dic.keys())

for k in dic.keys():
    print(f'key: {k}')

if 'blog' in dic.values():
    print('values is exist')
else:
    print('values is not exist')

print(dic.values())

for v in dic.values():
    print(f'value : {v}')

#전체를 다 뽑고 싶을 때
print(dic.items())

for i in dic.items():
    print(f'all : {i}')
    print(f'key : {i[0]}')
    print(f'value : {i[1]}')
    print()

v1 = dic.get('b')
print(f"dic.get['b'] : {v1}")

#값이 없으니까 null이 뜬다
v2 = dic.get('z')
print(f"dic.get['z'] : {v2}")

print(f'before : {dic}')

del dic['c']

print(f'after : {dic}')

dic.clear()
print(f'dic : {dic}')