const express = require("express");

const app = express();
const PORT = 8080;

app.get("/", (req, res) => {
  res.status(200).json({
    status: "success",
    message: "Server is healthy",
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


//   npm: '10.8.2',
//   node: '20.20.2'