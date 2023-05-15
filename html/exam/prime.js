onmessage = function (e) {
    let prime = parseInt(e.data.isprime); //e.data.number인가?
    let result = ""
    let i = 1;

    if (prime == 1) {
        result = "not prime number"
    } else if (prime == 2 || prime == 3) {
        result = "prime number"
    } else {
        for (i = 2; i < prime; i++)
            if (prime % i == 0) {
                result = "not prime number";
                break;

            } else {
                result = "prime number";
                break;

            }
        console.log(result)
    }
    postMessage(result);
} 