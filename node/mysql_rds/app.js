var express = require('express');
var mysql = require('mysql');
const env = require('dotenv').config({ path: "./.env" });

var connection = mysql.createConnection({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
})

var app = express();

connection.connect(function (err) {
    if (!err) {
        console.log("Database is connected .... \n\n");
    } else {
        console.log("Error connecting Database...\n\n");
    }
});

app.get('/', function (req, res) {
    connection.query('select * from st_info', function (err, rows, fields) {
        // connection.end();
        if (!err) {
            
            console.log(rows);
            res.writeHead(200);
            var template = `
          <!doctype html>
          <html>
          <head>
            <title>Result</title>
            <meta charset="utf-8">
          </head>
          <body>
           <table border="1" margin:auto; text-align:center;>
             <tr>
               <th>ST_ID</th>
               <th>NAME</th>
               <th>DEPT</th>
             </tr>
           `;
            for (var i = 0; i < rows.length; i++) {
                template += `
             <tr>
               <th>${rows[i]['ST_ID']}</th>
               <th>${rows[i]['NAME']}</th>
               <th>${rows[i]['DEPT']}</th>
             </tr>
            `
            }
            template += `
             </table>
          </body>
          </html>
         `;
            res.end(template);
        } else {
            console.log('Error while performing Query ');
        }
    })
})

app.listen(8000, function () {
    console.log('8000 Port : Server Started...');
})