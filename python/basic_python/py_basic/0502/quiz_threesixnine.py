numbers = (i for i in range(1,101))

a=list(numbers)

# for j in range(len(a)):
#     if "33" in str(a[j]) or "36" in str(a[j]) or "39" in str(a[j])or "63" in str(a[j])or "66" in str(a[j])or "69" in str(a[j])or "93" in str(a[j])or "96" in str(a[j])or "99" in str(a[j]):
#         print('👏👏',end='  ')
#     elif "0" in str(a[j]):
#         print(f'{a[j]}')
#     elif "3" in str(a[j]) or "6" in str(a[j]) or "9" in str(a[j]):
#         print('👏',end='  ')
#     else:
#         print(f'{a[j]}',end='  ')

##숫자로 표현
for x in range(len(a)):
    fir=int(a[x]%10)
    sec=int(a[x]%100/10)
    if a[x]%10==1:
        print()
    if (fir==3 or fir==6 or fir==9) & (sec==3 or sec==6 or sec==9):
        print("👏👏",end=' ')
    elif (fir==3 or fir==6 or fir==9) & (sec!=3 or sec!=6 or sec!=9):
        print("👏",end=' ')
    elif (fir!=3 or fir!=6 or fir!=9) & (sec==3 or sec==6 or sec==9):
        print("👏",end=' ')
    else:
        print(f"{a[x]}",end=' ')