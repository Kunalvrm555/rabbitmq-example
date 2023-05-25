const express = require('express');
const multer = require('multer');
const app = express();
const upload = multer({ dest: 'uploads/' });
const { sendMessage } = require('./publisher');

app.post('/upload', upload.single('file'), async (req, res) => {
  const { file } = req;

  // Send message to RabbitMQ
  try {
    const message = { fileId: file.filename, originalName: file.originalname };
    // console.log(message);
    await sendMessage(message);
    // mQ.send({
    //   topic: "DOC_GEN",
    //   payload: {
    //     type: "TDS",
    //     doc_gen_id: "1
    //   }
    // });

    console.log('Message sent to RabbitMQ');
  } catch (error) {
    console.error('Error sending message to RabbitMQ:', error);
  }

  res.send('File uploaded successfully');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
