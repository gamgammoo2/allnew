def prime(a):
    if a<=1:
        return 0
    elif a ==2 or a==3:
        return 1
    else :
        for i in range(2,(a//2)):
            if a%i==0:
                return 2
            else:
                return 1
