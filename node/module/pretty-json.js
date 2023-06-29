const prettier = require('prettier')

#제이슨을 예쁘게 보여주는 것(지금 상태는 완벽 소스는 아님)

res.json(prettier.format(JSON.stringify(object)));
