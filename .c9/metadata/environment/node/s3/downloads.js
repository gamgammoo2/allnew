{"filter":false,"title":"downloads.js","tooltip":"/node/s3/downloads.js","undoManager":{"mark":27,"position":27,"stack":[[{"start":{"row":0,"column":0},"end":{"row":22,"column":23},"action":"insert","lines":["const fs = require('fs')","const env = require('dotenv').config({path:\"../../.env\"});","","const AWS = require('aws-sdk');","const ID =process.env.ID;","const SECRET =process.env.SECRET;","const BUCKET_NAME = 'gam-0858';","const MYREGION = 'ap-northeast-2';","const s3 = new AWS.S3({accessKeyID : ID, secretAccessKey: SECRET, region: MYREGION});","","const uploadFile = (fileName) => {","    const fileContent = fs.readFileSync(fileName);","    const params = {","        Bucket: BUCKET_NAME,","        Key:'axios.png',","        Body: fileContent","    };","    s3.upload(params, function(err,data) {","        if (err) { throw err; }","        console.log(`File uploaded successfully. ${data.Location}`);","    });","}","uploadFile('axios.png')"],"id":1}],[{"start":{"row":10,"column":6},"end":{"row":10,"column":11},"action":"remove","lines":["uploa"],"id":2}],[{"start":{"row":10,"column":6},"end":{"row":10,"column":7},"action":"insert","lines":["d"],"id":3},{"start":{"row":10,"column":7},"end":{"row":10,"column":8},"action":"insert","lines":["o"]},{"start":{"row":10,"column":8},"end":{"row":10,"column":9},"action":"insert","lines":["w"]},{"start":{"row":10,"column":9},"end":{"row":10,"column":10},"action":"insert","lines":["n"]},{"start":{"row":10,"column":10},"end":{"row":10,"column":11},"action":"insert","lines":["l"]},{"start":{"row":10,"column":11},"end":{"row":10,"column":12},"action":"insert","lines":["o"]},{"start":{"row":10,"column":12},"end":{"row":10,"column":13},"action":"insert","lines":["a"]}],[{"start":{"row":11,"column":4},"end":{"row":11,"column":50},"action":"remove","lines":["const fileContent = fs.readFileSync(fileName);"],"id":4},{"start":{"row":11,"column":0},"end":{"row":11,"column":4},"action":"remove","lines":["    "]},{"start":{"row":10,"column":36},"end":{"row":11,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":14,"column":8},"end":{"row":14,"column":25},"action":"remove","lines":["Body: fileContent"],"id":5},{"start":{"row":14,"column":4},"end":{"row":14,"column":8},"action":"remove","lines":["    "]},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"remove","lines":["    "]},{"start":{"row":13,"column":24},"end":{"row":14,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":13,"column":23},"end":{"row":13,"column":24},"action":"remove","lines":[","],"id":6}],[{"start":{"row":15,"column":7},"end":{"row":15,"column":13},"action":"remove","lines":["upload"],"id":7},{"start":{"row":15,"column":7},"end":{"row":15,"column":8},"action":"insert","lines":["g"]},{"start":{"row":15,"column":8},"end":{"row":15,"column":9},"action":"insert","lines":["e"]},{"start":{"row":15,"column":9},"end":{"row":15,"column":10},"action":"insert","lines":["t"]},{"start":{"row":15,"column":10},"end":{"row":15,"column":11},"action":"insert","lines":["O"]}],[{"start":{"row":15,"column":11},"end":{"row":15,"column":12},"action":"insert","lines":["b"],"id":8},{"start":{"row":15,"column":12},"end":{"row":15,"column":13},"action":"insert","lines":["j"]},{"start":{"row":15,"column":13},"end":{"row":15,"column":14},"action":"insert","lines":["e"]},{"start":{"row":15,"column":14},"end":{"row":15,"column":15},"action":"insert","lines":["c"]},{"start":{"row":15,"column":15},"end":{"row":15,"column":16},"action":"insert","lines":["t"]}],[{"start":{"row":16,"column":31},"end":{"row":17,"column":0},"action":"insert","lines":["",""],"id":9},{"start":{"row":17,"column":0},"end":{"row":17,"column":8},"action":"insert","lines":["        "]},{"start":{"row":17,"column":8},"end":{"row":17,"column":9},"action":"insert","lines":["f"]},{"start":{"row":17,"column":9},"end":{"row":17,"column":10},"action":"insert","lines":["s"]},{"start":{"row":17,"column":10},"end":{"row":17,"column":11},"action":"insert","lines":["."]},{"start":{"row":17,"column":11},"end":{"row":17,"column":12},"action":"insert","lines":["w"]},{"start":{"row":17,"column":12},"end":{"row":17,"column":13},"action":"insert","lines":["r"]},{"start":{"row":17,"column":13},"end":{"row":17,"column":14},"action":"insert","lines":["i"]}],[{"start":{"row":17,"column":14},"end":{"row":17,"column":15},"action":"insert","lines":["t"],"id":10},{"start":{"row":17,"column":15},"end":{"row":17,"column":16},"action":"insert","lines":["e"]},{"start":{"row":17,"column":16},"end":{"row":17,"column":17},"action":"insert","lines":["r"]},{"start":{"row":17,"column":17},"end":{"row":17,"column":18},"action":"insert","lines":["F"]},{"start":{"row":17,"column":18},"end":{"row":17,"column":19},"action":"insert","lines":["i"]},{"start":{"row":17,"column":19},"end":{"row":17,"column":20},"action":"insert","lines":["l"]},{"start":{"row":17,"column":20},"end":{"row":17,"column":21},"action":"insert","lines":["e"]}],[{"start":{"row":17,"column":21},"end":{"row":17,"column":22},"action":"insert","lines":["S"],"id":11},{"start":{"row":17,"column":22},"end":{"row":17,"column":23},"action":"insert","lines":["y"]},{"start":{"row":17,"column":23},"end":{"row":17,"column":24},"action":"insert","lines":["n"]},{"start":{"row":17,"column":24},"end":{"row":17,"column":25},"action":"insert","lines":["c"]}],[{"start":{"row":17,"column":25},"end":{"row":17,"column":27},"action":"insert","lines":["()"],"id":12}],[{"start":{"row":17,"column":26},"end":{"row":17,"column":27},"action":"insert","lines":["f"],"id":13},{"start":{"row":17,"column":27},"end":{"row":17,"column":28},"action":"insert","lines":["i"]},{"start":{"row":17,"column":28},"end":{"row":17,"column":29},"action":"insert","lines":["l"]},{"start":{"row":17,"column":29},"end":{"row":17,"column":30},"action":"insert","lines":["e"]},{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"insert","lines":["n"]},{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"insert","lines":["a"]},{"start":{"row":17,"column":32},"end":{"row":17,"column":33},"action":"insert","lines":["m"]},{"start":{"row":17,"column":33},"end":{"row":17,"column":34},"action":"insert","lines":["e"]},{"start":{"row":17,"column":34},"end":{"row":17,"column":35},"action":"insert","lines":[","]}],[{"start":{"row":17,"column":34},"end":{"row":17,"column":35},"action":"remove","lines":[","],"id":14},{"start":{"row":17,"column":33},"end":{"row":17,"column":34},"action":"remove","lines":["e"]},{"start":{"row":17,"column":32},"end":{"row":17,"column":33},"action":"remove","lines":["m"]},{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"remove","lines":["a"]},{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"remove","lines":["n"]}],[{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"insert","lines":["A"],"id":15},{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"insert","lines":["n"]},{"start":{"row":17,"column":32},"end":{"row":17,"column":33},"action":"insert","lines":["e"]},{"start":{"row":17,"column":33},"end":{"row":17,"column":34},"action":"insert","lines":["m"]}],[{"start":{"row":17,"column":33},"end":{"row":17,"column":34},"action":"remove","lines":["m"],"id":16},{"start":{"row":17,"column":32},"end":{"row":17,"column":33},"action":"remove","lines":["e"]},{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"remove","lines":["n"]},{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"remove","lines":["A"]}],[{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"insert","lines":["A"],"id":17},{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"insert","lines":["N"]}],[{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"remove","lines":["N"],"id":18},{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"remove","lines":["A"]}],[{"start":{"row":17,"column":30},"end":{"row":17,"column":31},"action":"insert","lines":["N"],"id":19},{"start":{"row":17,"column":31},"end":{"row":17,"column":32},"action":"insert","lines":["a"]},{"start":{"row":17,"column":32},"end":{"row":17,"column":33},"action":"insert","lines":["m"]},{"start":{"row":17,"column":33},"end":{"row":17,"column":34},"action":"insert","lines":["e"]},{"start":{"row":17,"column":34},"end":{"row":17,"column":35},"action":"insert","lines":[","]}],[{"start":{"row":17,"column":35},"end":{"row":17,"column":36},"action":"insert","lines":["d"],"id":20},{"start":{"row":17,"column":36},"end":{"row":17,"column":37},"action":"insert","lines":["a"]},{"start":{"row":17,"column":37},"end":{"row":17,"column":38},"action":"insert","lines":["t"]},{"start":{"row":17,"column":38},"end":{"row":17,"column":39},"action":"insert","lines":["a"]},{"start":{"row":17,"column":39},"end":{"row":17,"column":40},"action":"insert","lines":["."]},{"start":{"row":17,"column":40},"end":{"row":17,"column":41},"action":"insert","lines":["B"]},{"start":{"row":17,"column":41},"end":{"row":17,"column":42},"action":"insert","lines":["o"]},{"start":{"row":17,"column":42},"end":{"row":17,"column":43},"action":"insert","lines":["d"]},{"start":{"row":17,"column":43},"end":{"row":17,"column":44},"action":"insert","lines":["y"]}],[{"start":{"row":18,"column":8},"end":{"row":18,"column":68},"action":"remove","lines":["console.log(`File uploaded successfully. ${data.Location}`);"],"id":21},{"start":{"row":18,"column":4},"end":{"row":18,"column":8},"action":"remove","lines":["    "]},{"start":{"row":18,"column":0},"end":{"row":18,"column":4},"action":"remove","lines":["    "]},{"start":{"row":17,"column":45},"end":{"row":18,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":20,"column":0},"end":{"row":20,"column":2},"action":"remove","lines":["up"],"id":22},{"start":{"row":20,"column":0},"end":{"row":20,"column":1},"action":"insert","lines":["d"]},{"start":{"row":20,"column":1},"end":{"row":20,"column":2},"action":"insert","lines":["o"]},{"start":{"row":20,"column":2},"end":{"row":20,"column":3},"action":"insert","lines":["w"]},{"start":{"row":20,"column":3},"end":{"row":20,"column":4},"action":"insert","lines":["n"]}],[{"start":{"row":20,"column":25},"end":{"row":20,"column":26},"action":"insert","lines":[";"],"id":23}],[{"start":{"row":15,"column":10},"end":{"row":15,"column":11},"action":"remove","lines":["O"],"id":24}],[{"start":{"row":15,"column":10},"end":{"row":15,"column":11},"action":"insert","lines":["O"],"id":25}],[{"start":{"row":1,"column":44},"end":{"row":1,"column":45},"action":"insert","lines":["."],"id":26},{"start":{"row":1,"column":45},"end":{"row":1,"column":46},"action":"insert","lines":["."]},{"start":{"row":1,"column":46},"end":{"row":1,"column":47},"action":"insert","lines":["/"]}],[{"start":{"row":1,"column":46},"end":{"row":1,"column":47},"action":"remove","lines":["/"],"id":27},{"start":{"row":1,"column":45},"end":{"row":1,"column":46},"action":"remove","lines":["."]},{"start":{"row":1,"column":44},"end":{"row":1,"column":45},"action":"remove","lines":["."]}],[{"start":{"row":17,"column":16},"end":{"row":17,"column":17},"action":"remove","lines":["r"],"id":28}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":4,"column":0},"end":{"row":8,"column":85},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":5,"state":"start","mode":"ace/mode/javascript"}},"timestamp":1686641392767,"hash":"62ccd4750b4eb6e199bba64eaa231e3c49f71994"}