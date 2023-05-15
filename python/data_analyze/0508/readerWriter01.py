myfile01 = open('sample.txt', 'rt', encoding='UTF-8')
linelists = myfile01.readlines()
myfile01.close()
print(linelists)

myfile2 = open('result.txt', 'wt', encoding='UTF-8')

total = 0 # 총점
for one in linelists :
    score = int(one)
    total += score
    myfile2.write('total=' + str(total) + ',value ='+str(score)+'\n')
average = total / len(linelists) # 평균


myfile2.write('총점 : ' + str(total) + '\n')
myfile2.write('평균 : ' + str(average))

myfile2.close()

myfile3=open('sample.txt', 'rt', encoding='UTF-8')
line=1
while line:
    line=myfile3.readline()
    print(line)
myfile3.close()

