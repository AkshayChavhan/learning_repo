// The "backend" that gets shipped to ECR (and later run on ECS).
// Nothing fancy on purpose: the lesson is the registry, not the app.
const express = require("express");

const app = express();
const PORT = Number(process.env.PORT || 8000);   // set by ENV PORT in the Dockerfile; ECS can override it

app.get("/", (req, res) => {
  res.json({
    status: "success",
    message: "backend is healthy",
    port: PORT,
    // handy when the same image runs in several places: which build answered?
    image: process.env.IMAGE_TAG || "local",
  });
});

app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
