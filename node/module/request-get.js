const https=require('https');

const options = {
    hostname : 'example.com',
    port : 3000,
    path : '/todos',
    method : 'GET'
}

const req = https.request(options, res => {
    console.log(`statusCode : ${res.statusCode}`)
    res.on('data', d => {
        process.stdout.write(d)
    })
})

res.on('error', error => {
    console.err(error)
})

req.end()
