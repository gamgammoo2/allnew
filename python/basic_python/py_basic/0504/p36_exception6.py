def division_function(a,b):
    try:
        print(a/b)
    except TypeError as e:
        return -1
    except ZeroDivisionError as e:
        return -2
    except Exception as e:
        return -3



ret=division_function("a",1)
print(ret)
ret=division_function(1,0)
print(ret)
# ret=division_function(4,2)
# print(ret) # 에러가 없어서 none이 나옴
#sql에서 쿼리를 성공했으면 성공 메시지를 내주고, 안했을 때 -> 각각의 에러 타입에 따라서 처리할 수 있다.
ret = division_function(4,2)
if ret!=None:
    print("Error")

#exception에는 순서가 있다. exceiption을 맨 마지막 예외로 처리해야 다른 애러들이 먹을 수 있다.