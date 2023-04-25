const axios = require('axios');

axios
    .post('http://192.168.1.183:8000/todos', {
        todo: "I NEED RICE 3KG -GAM"
    })
    .then(res => {
        console.log(`statusCode : ${res.status}`)
        console.log(res)
    })
    .catch(error => {
        console.log(error)
    })