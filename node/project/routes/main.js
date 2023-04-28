const express = require('express');
const bodyParser = require('body-parser');
const pool = require("../../config/pool");

const mongoose = require("mongoose")

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//show today's H vs A
app.get('/main/today', (req, res) => {
    res.send('A vs B')
})

//user관리
// all user select
// app.get('/user/select', (req, res) => {
//     const result = connection.query('select * from dataUser');
//     console.log(result);
//     res.send({ "ok": true, "result": result });
//     //, "affectedRows":' + result.affectedRows + ', "service":"insert"
// })

// //select from userID
// app.get('/select/userID', (req, res) => {
//     const userID = req.query.userID;
//     const result = connection.query('select * from dataUser where userID=?', [userID]);
//     console.log(result);
//     res.send({ "ok": true, "result": result });
// })

//user screen home,away->kia,doosan select
app.get('/selectHA', async (req, res) => {
    let rows = ""
    const { Home, Away } = req.query;
    if (Home == "" && Away != "") {
        [rows, fields] = await pool.query("select * from dataSchedule where away=?", [Away])
    } else if (Home != "" && Away == "") {
        [rows, fields] = await pool.query("select * from dataSchedule where home =?", [Home])
    } else {
        [rows, fields] = await pool.query("select * from dataSchedule where home =? and away=?", [Home, Away])
    }
    console.log(rows)
    res.send({ 'ok': true, 'result': rows[0] });
})

//MY SQL + MONGO  for bookingpage
async function mysqlbook(req) {
    const month = req.query.month;
    const [rows, fields] = await pool.query('SELECT * FROM dataSchedule where substr(날짜,1,2)=?', [month]);
    return rows;
}

//mongo sql booking
app.get('/booking', (req, res) => {
    res.writeHead(200);
    var template = `
      <!DOCTYPE html>
<html lang="ko">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>야구 경기 예매</title>
  <link rel="stylesheet" href="booking.css" />
  
</head>

<body>
  <header>
    <h1>야구 예매</h1>
  </header>
  <main>

    <section class="ticket-selection">
      <h2>좌석 선택</h2>
      <div>
        <label for="selectTeam">구단:</label>
        <select id="selectTeam">
          <option value="" disabled selected>구단을 선택하세요</option>
          <option value="doosan">두산 베어스</option>
          <option value="kia">기아 타이거즈</option>
        </select>
      </div>
      <div>
        <label for="selectSeat">좌석:</label>
        <select id="selectSeat">
          <option value="" disabled selected>좌석을 선택하세요</option>
          <option value="1">레드존</option>
          <option value="2">블루존</option>
        </select>
      </div>
      <div>
        <label for="selectSeatNum">좌석 번호:</label>
        <select id="selectSeatNum">
          <option value="" disabled selected>좌석 번호를 선택하세요</option>
          <option value="1">1111</option>
        </select>
        <div>
          <label for="selectWeekday">요일:</label>
          <select id="selectWeekday">
            <option value="" disabled selected>요일을 선택하세요</option>
            <option value="weekday">주중</option>
            <option value="weekend">주말</option>
          </select>
        </div>
        <form id="ticketForm" onsubmit="event.preventDefault();">
          <label for="ticketCount">티켓 수:</label>
          <input type="number" id="ticketCount" name="ticketCount" min="1" value="1" />
          <div id="clickbooking">
            <button type="submit">예매하기</button>
          </div>
        </form>
    </section>
    <div class="back">
      <ul>
        <li style="list-style: none;"><a href="login.html">뒤로가기</a></li>
      </ul>
    </div>
    
  </main>
  
  </body>
</html>
            `;
    res.end(template);
})







module.exports = app;