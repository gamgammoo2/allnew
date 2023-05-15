try:
    f = open("test1.txt", "r")
except IOError as e :
    print(e)
finally:
    data = f.readline()
    print(data)
    f.close()
#당연히 에러를 낸거임