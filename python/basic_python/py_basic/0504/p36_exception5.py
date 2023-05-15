def division_function(a,b):
    try:
        print(a/b)
    except TypeError as e:
        print('2nd')
    except ZeroDivisionError as e:
        print('3rd')
    except Exception as e:
        print('1st')



division_function("a",1)
division_function(1,0)
division_function(4,2)

#exception에는 순서가 있다. exceiption을 맨 마지막 예외로 처리해야 다른 애러들이 먹을 수 있다.