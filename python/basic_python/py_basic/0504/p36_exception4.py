def division_function(a,b):
    try:
        print(a/b)
    except Exception as e:
        print('1st')
    except TypeError as e:
        print('2nd')
    except ZeroDivisionError as e:
        print('3rd')

division_function("a",1)
division_function(1,0)
division_function(4,2)

#exception이 큰 범주임. 그래서 얘한테 걸리먼 얘가 다 처리해버림