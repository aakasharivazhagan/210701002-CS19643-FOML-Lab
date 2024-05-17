const express = require('express')
const cors =require('cors')
const fs = require('fs');
const axios = require('axios');
const { spawn } = require('child_process');
const PORT = process.env.PORT || 3500;

const app = express();

app.use(express.json());
app.use(cors());

app.get('/', (req, res)=>{
    res.send("the infamous / route.. ");
})

app.get('/schemes', (req, res) => {
    fs.readFile('./Datasets/.json', 'utf8', (err, data) => {
      if (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
        return;
      }
      const jsonData = JSON.parse(data);
      res.json(jsonData);
    });
  });

// POST REQ
 /*[
    {
        "role": "user",
        "content": "tell me about the schemes in agricultural department"
    }
] */

app.post('/', async(req, res)=>{
  const pythonScriptPath = './Python-modules/api.py';
  const inputData = req.body;

  // res to axios
  const content = inputData.content;
  console.log('Received data from React:', inputData);

  const scriptArgs = [pythonScriptPath, JSON.stringify(inputData)];
  const pythonProcess = spawn('python', scriptArgs);

  let scriptOutput = '';
  pythonProcess.stdout.on('data', (data) => {
    scriptOutput += data.toString();
  });

  pythonProcess.on('error', (error) => {
    console.error('error in python script:', error);
    res.status(500).send('internal error');
  });

  pythonProcess.on('close', (code) => {
    console.log(`python api script exited with code ${code}`);
    res.send(scriptOutput);
    console.log('Received data from Express:', scriptOutput);
    
  });

  // const receivedData = req.body;
  //   console.log('Received data from React:', receivedData);
  //   res.json({ message: 'Data received by Express!' });


});




  // app.post('/', async (req, res) => {
  //   try {
  //     // Get the array of JSON objects from the request body
  //     const jsonData = req.body;
  
  //     // Perform any necessary validation on the data
  
  //     // Construct the payload in the required format
  //     const nagaApiPayload = {
  //       model: 'gpt-3.5-turbo-1106',
  //       messages: jsonData.messages,
  //     };
  
  //     // Make a POST request to the Naga API
  //     const nagaApiKey = 'ng-h6Y9mCjggLaYzkklJvZzMljBB3Sh6';
  //     const nagaApiUrl = 'https://api.naga.ac/v1/chat/completions'; // Replace with the actual Naga API endpoint
  
  //     const responseFromNaga = await axios.post(nagaApiUrl, nagaApiPayload, {
  //       headers: {
  //         'Content-Type': 'application/json',
  //         'X-API-Key': nagaApiKey,
  //       },
  //     });
  
  //     // Handle the response from the Naga API
  //     const nagaApiResponseData = responseFromNaga.data;
  
  //     // Save the received data or do any additional processing
  
  //     // Send the Naga API response back to the user
  //     res.status(200).json({
  //       success: true,
  //       message: 'Data sent to Naga API successfully.',
  //       nagaApiResponse: nagaApiResponseData,
  //     });
  //   } catch (error) {
  //     console.error('Error:', error.message);
  //     res.status(500).json({ success: false, message: 'Internal Server Error' });
  //   }
  // });

app.listen(PORT, ()=>{
    console.log("Server started at "+ PORT);
})