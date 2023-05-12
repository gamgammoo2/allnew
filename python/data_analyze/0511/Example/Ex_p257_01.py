import urllib.request

url = "https://mblogthumb-phinf.pstatic.net/MjAyMDA5MzBfMTQz/MDAxNjAxNDU0NjQ2MTQ2.j4BF8brAORpqM95d7-_yolEFGB-kEvZRqDZ3MZtD9ekg.AfCQ6EZbvdwRg0_BA-73lN2grfPCBoFBJ2ubhYENy9sg.JPEG.yunny_23/3D056E1A-9BB0-40C8-9046-9EB7B48E98E3-323-0000003CDE7A5723_file.jpg?type=w800"

savename=input('저장할 파일 이름 입력 :')


result=urllib.request.urlopen(url) #byte로 나오게 하려고
data=result.read()
print('# type(data) :', type(data))

with open(savename, mode='wb') as f:
    f.write(data)
    print(savename + 'saved...')