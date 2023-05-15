#pass를 왜쓸까? 비어있는 구문이 있을 수 있음 ex) try except else finally 구문이나/ elif가 필요한데 당장 넣을 게 없을때, 일단 넣어두는 것.
sum=0
for i in range(10):
    if i %2==0:
        pass
    sum += i
    print(f'sum += {i}')
print()
print(f'sum = {sum}')