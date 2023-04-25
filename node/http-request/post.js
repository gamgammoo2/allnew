const https = require('https');

const data = JSON.stringify({
    todo: 'Buy the rice-GAM'
})

const options = {
    hostname: '192.168.1.183',
    port: 8000,
    path: '/todos',
    method: 'POST',
    header: { //post에는 header가 들어감
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
}

const req = https.request(options, res => {
    console.log(`statusCode : ${res.statusCode}`);
    res.on('data', d => {
        process.stdout.write(d);
    })
})

req.on('error', error => {
    console.log(error)
})

req.write(data)
req.end()