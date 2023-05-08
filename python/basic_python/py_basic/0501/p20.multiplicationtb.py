while True:
    i=input("input the number (q : Quit) : ")

    if i =='q':
        break
    elif (int(i)<2 or int(i)>9):
        break
    else:
        for j in range(1,10):
            print(f'{i}*{j}={int(i)*j}')