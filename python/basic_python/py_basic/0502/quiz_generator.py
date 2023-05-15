mynum=[1,2,3,4,5]

def square():
    i=0
    while i< len(mynum):
        yield mynum[i]**2
        i+=1
    return

result=square()

for i in range(1,len(mynum)+1):
    print(f"Square value of mynum[{i-1}] = {i} : ",result.__next__())

# print(result.__next__())
# print(result.__next__())
# print(result.__next__())
# print(result.__next__())
# print(result.__next__())

