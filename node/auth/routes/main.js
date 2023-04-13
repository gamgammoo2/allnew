const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: '../../.env' });

var connection = new mysql({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database,
});

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


// request 있다1, query 없다0
app.get('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
});

// request1, query 0
app.post('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
});

// request 1, query 1
app.get('/selectQuery', (req, res) => {
    const userid = req.query.userid;
    const result = connection.query('SELECT * FROM user where userid=?', [userid]);
    console.log(result);
    res.send(result);
});

// request 1, query 1
app.post('/selectQuery', (req, res) => {
    const userid = req.body.userid;
    const result = connection.query('SELECT * FROM user where userid=?', [userid]);
    console.log(result);
    res.send(result);
});

// request 1, query 1
app.post('/insert', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("insert into user values (?,?)", [id, pw]);
    console.log(result);
    res.redirect('/selectQuery?userid=' + req.body.id);
});

// request 1, query 1
app.post('/update', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("update user set passwd=? where userid=?", [pw, id]);
    console.log(result);
    res.redirect('/selectQuery?userid=' + req.body.id);
});

// request 1, query 1
app.post('/delete', (req, res) => {
    const id = req.body.id;
    const result = connection.query("delete from user where userid=?", [id]);
    console.log(result);
    res.redirect('/select');
});
//-----------------------------------------------------------------------

// register
app.post("/success", (req, res) => {
    const { id, pw } = req.body;
    if (id == "") {
        res.redirect("register.html");
    } else {
        let result = connection.query("select * from user where userid=?", [id]);
        if (result.length > 0) {
            res.writeHead(200);
            var template = `
            <!doctype html>
            <html>
            <head>
                <title>Error</title>
                <meta charset="utf-8">
            </head>
            <body>
                <div class="box3">
                    <h3 style="margin-left: 30px">Register Failed</h3>
                    <h4 style="margin-left: 30px">이미 존재하는 아이디입니다.</h4>
                    <a href="register.html" style="margin-left: 30px">다시 시도하기</a>
                </div>
            </body>
            </html>
            `;
            res.end(template);
        } else {
            result = connection.query("insert into user values (? ,?)", [id, pw]);
            console.log(result);
            res.redirect("/");
        }
    }
});

// request O, query X
app.get("/select", (req, res) => {
    const result = connection.query("select * from user");
    console.log(result);
    res.send(result);
});

// request 1, query 1
app.post('/find', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("SELECT * FROM user where userid=? and passwd=?", [id, pw]);
    if (result.length == 0) {
        res.redirect('error.html')
    }
    if (id == 'admin' || id == 'root') {
        console.log(id + " >>>> 관리자 로그인함")
        res.redirect("member.html")
    } else {
        console.log(id + " >>>> 유저 로그인함")
        res.redirect('gohome.html')
    }
});


module.exports = app;