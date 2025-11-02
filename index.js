const express = require('express');

const app = express();
const port = 8000;

// define a simple route at the base directory, "/", the response is the same
//  and the request information is not necessary
app.get('/', (req, res) => {
  res.send('API is running!');
});

// start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});