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
    //res.send(result);
    res.writeHead(200);
    var template = `
       <!doctype html>
       <html>
       <head>
           <title>Result</title>
           <meta charset="utf-8">
           <style>
table { /* 이중 테두리 제거 */
	border-collapse : collapse; 
}
td, th { /* 모든 셀에 적용 */
	text-align : center;
	padding : 5px;
	height : 15px;
	width : 100px;
}
thead, tfoot { /* <thead>의 모든 셀에 적용 */
	background : black;
	color : white;
}
tbody tr:nth-child(even) { /* 짝수 <tr>에 적용*/
	background : lightgray;
}
tbody tr:hover { /* 마우스가 올라오면 pink 배경 */
	background : lightblue;	
}
</style>
       </head>
       <body>
       <table border="1" style="margin:auto; text-align:center;">
       <thead>
           <tr><th>User ID</th><th>Password</th></tr>
       </thead>
       <tbody>
       `;
    for (var i = 0; i < result.length; i++) {
        template += `
       <tr>
           <td>${result[i]['userid']}</td>
           <td>${result[i]['passwd']}</td>
       </tr>
       `;
    }
    template += `
       </tbody>
       </table>
       </body>
       </html>
   `;
    res.end(template);
})

// request1, query 0
app.post('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
});

// request 1, query 1
app.get('/selectQuery', (req, res) => {
    const id = req.query.id;
    const result = connection.query("SELECT * FROM user where userid=?", [id]);
    console.log(result);
    if (id == '') {
        //res.send("입력을 확인해주세요");
        res.write("<script>alert('입력을 확인했나요 휴먼~~~?')</script>")
    } else {
        if (result.length == 0) {
            res.send("테이블에 존재하지 않습니다.")
        }
        else {
            res.writeHead(200);
            var template = `
       <!doctype html>
       <html>
       <head>
           <title>Result</title>
           <meta charset="utf-8">
           <style>
table { /* 이중 테두리 제거 */
	border-collapse : collapse; 
}
td, th { /* 모든 셀에 적용 */
	text-align : center;
	padding : 5px;
	height : 15px;
	width : 100px;
}
thead, tfoot { /* <thead>의 모든 셀에 적용 */
	background : black;
	color : white;
}
tbody tr:nth-child(even) { /* 짝수 <tr>에 적용*/
	background : lightgray;
}
tbody tr:hover { /* 마우스가 올라오면 pink 배경 */
	background : lightblue;	
}
</style>
       </head>
       <body>
       <table border="1" style="margin:auto; text-align:center;">
       <thead>
           <tr><th>User ID</th><th>Password</th></tr>
       </thead>
       <tbody>
       `;
            for (var i = 0; i < result.length; i++) {
                template += `
       <tr>
           <td>${result[i]['userid']}</td>
           <td>${result[i]['passwd']}</td>
       </tr>
       `;
            }
            template += `
       </tbody>
       </table>
       </body>
       </html>
   `;
        }
        res.end(template);
    }
})



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
    if (id == "" || pw == "") {
        res.write("<script>alert('입력을 확인했나요 휴먼~~~?')</script>");;
    } else {
        let result = connection.query("select * from user where userid=?", [id]);
        if (result.length != 0) {
            res.write("<script>alert('이런...휴먼...이미 있는 사람이잖슴...')</script>");
        }
        else {
            const result = connection.query("insert into user values (?,?)", [id, pw]);
            console.log(result);
            res.redirect('/selectQuery?id=' + id);
        }
    }
})

// request 1, query 1
app.post('/update', (req, res) => {
    const { id, pw } = req.body;
    if (id == "" || pw == "") {
        res.write("<script>alert('입력을 확인했나요 휴먼~~~?')</script>");
    } else {
        let result = connection.query("select * from user where userid=?", [id]);
        if (result.length == 0) {
            res.write("<script>alert('휴먼...또...이런다...없는 놈을 내가 어찌 넣을까?? 영원히 휴면하고싶어 휴먼?')</script>");
        }
        else {
            const result = connection.query("update user set passwd=? where userid=?", [pw, id]);
            console.log(result);
            res.redirect('/selectQuery?id=' + id);
        }
    }
})

// request 1, query 1
app.post('/delete', (req, res) => {
    const id = req.body.id;
    if (id == "") {
        res.write("<script>alert('입력을 확인했나요 휴먼~~~?')</script>");
    } else {
        const result = connection.query("select * from user where userid=?", [id]);
        if (result.length == 0) {
            res.write("<script>alert('휴먼...또...이런다...없는 놈을 내가 어찌 뺄까?? 영원히 휴면하고싶어 휴먼?')</script>");
        } else {
            const result = connection.query("delete from user where userid=?", [id]);
            console.log(result);
            res.redirect('/select');
        }
    }

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