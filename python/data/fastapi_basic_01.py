from fastapi import FastAPI

app=FastAPI()

@app.get('/')
async def healthCheck():
    return "OK"

@app.get('/hello')
async def Hello():
    return "Hello yo~~!"

@app.post('/random') #post로 만들기
@app.get('/random')
async def random(max=None):
    import random
    if max is None:
        max=10
    else:
        max=int(max)
    random_v = random.randint(1,max)

    return random_v