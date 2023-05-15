while True:
    i=input("input the number (q : Quit) : ")

    if i =='q':
        break
    else:
        if int(i) > 0:
            print("this is positive")
        elif int(i) ==0:
            print("this is zero")
        else:
            print("this is negative")