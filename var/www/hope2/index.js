//Node Modules
const express = require('express');
const multer = require('multer');
const util = require('util');
const vision = require('@google-cloud/vision');
//Global Variables
//const client = new vision.ImageAnnotatorClient();
const PORT = 8080;
const app = express();
const storage = multer.diskStorage({
  destination: function(req,file,cb){
    cb(null,'./upload');
  },
  filename: function(req,file,cb){
    cb(null,file.fieldname + '-' + Date.now()+'.'+file.mimetype.split('/')[1]);
  }
});
const upload = multer({storage:storage});

app.use(express.static('public'));


app.get('/',function(req,res){
  res.render('index.ejs');
});

app.post('/upload',upload.single('image_input'),function(req,res){
  const file = req.file;
  if(!file){
    res.write('nofile')//error handle
  }else{
    exportDetections(file.path).then((detections) => {res.write(detections);
    res.end();});
  }
});

app.listen(PORT, function(){
  console.log('Listening to '+PORT);
});

function exportDetections(fileName) {
    // Creates a client
    const client = new vision.ImageAnnotatorClient();

    // Performs text detection on the local file
    return client
      .textDetection(fileName)
      .then(results => {
        const detections = results[0].fullTextAnnotation.text;
        return detections;
      });
}

/*
function main(fileName){
  const vision = require('@google-cloud/vision');
  const client = new vision.ImageAnnotatorClient();
  const result = client.textDetection(fileName);
  return new Promise(result)i;
};
*/
