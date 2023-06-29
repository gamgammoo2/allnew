const express    = require('express');
const app        = express.Router();
const multer = require("multer")
const fs = require("fs")

var storage = multer.diskStorage({
  destination(req, file, cb) {
    cb(null, 'uploadedFiles/');
  },
  filename(req, file, cb) {
    cb(null, `${Date.now()}__${file.originalname}`);
  },
});

var upload = multer({ dest : 'uploadedFiles/' });
var uploadWithOriginalFilename = multer({ storage : storage });

app.get('/', function(req, res) {
  res.render('upload');
});

app.post('/uploadFile', upload.single('attachment'), function (req, res) {
  res.render('confirmation', { file:req.file, files:null });
});

app.post('/uploadFileWithOriginalFilename', uploadWithOriginalFilename.single('attachment'), function (req, res) {
  res.render('confirmation', { file:req.file, files:null });
});

app.post('/uploadFiles', upload.array('attachments'), function (req, res) {
  res.render('confirmation', { file:null, files:req.files });
});

app.post('/uploadFilesWithOriginalFilename', uploadWithOriginalFilename.array('attachments'), function (req, res) {
  res.render('confirmation', { file:null, files:req.files });
});

app.post('/downloadfile', function(req,res) {
  res.filename = req.body.dlKey
  console.log(filename);
  const downloadfile = (filename) => {
    const params = {
    Key: filename
  };
  getObject(params, function(err,data) {
    if (err) { return console.log(err); }
    res.attachment(filename);
    res.send(data.Body);
    res.end();
  })
  }
  downloadFile(filename);
})

app.get('/list', (req, res) => {
    const fullPath = process.cwd() + '/uploadedFiles' //(not __dirname)
    const dir = fs.opendirSync(fullPath)
    let entity
    let listing = []
    while((entity = dir.readSync()) !== null) {
        if(entity.isFile()) {
            listing.push({ type: 'f', name: entity.name })
        } else if(entity.isDirectory()) {
            listing.push({ type: 'd', name: entity.name })
        }
    }
    dir.closeSync()
    res.send(listing)
})

module.exports = app;
