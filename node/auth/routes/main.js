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

// request 1, query 1
app.post('/success', (req, res) => {
    const { id, pw } = req.body;
    const result = connection.query("insert into user values (?,?)", [id, pw]);
    console.log(result);
    res.redirect('/success.html');
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
        res.redirect('user.html')
    }
});


module.exports = app;