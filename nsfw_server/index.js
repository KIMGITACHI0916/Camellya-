const express = require("express");
const tf = require("@tensorflow/tfjs-node");
const nsfw = require("nsfwjs");
const app = express();
const PORT = 5000;

app.use(express.json({ limit: "5mb" }));

let model;

(async () => {
  model = await nsfw.load(); // Load model on startup
  console.log("NSFW model loaded.");
})();

app.post("/classify", async (req, res) => {
  try {
    const imageBuffer = Buffer.from(req.body.image, "base64");
    const image = tf.node.decodeImage(imageBuffer, 3);
    const predictions = await model.classify(image);
    image.dispose();
    res.json(predictions);
  } catch (err) {
    res.status(500).json({ error: "Failed to classify image." });
  }
});

app.listen(PORT, () => console.log(`NSFW server running on port ${PORT}`));
