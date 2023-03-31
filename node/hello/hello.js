const express = require('express');
const app = express();

app.get('/', function (req, res) {
    res.send("Hello Node js")
});

app.listen(3000, function () {
    console.log("3000 port : Server Start~!!")
});

