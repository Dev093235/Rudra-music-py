const express = require("express");
const ytdl = require("ytdl-core");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());

app.get("/", (req, res) => {
  res.send("✅ YouTube Downloader API by Rudra is running.");
});

app.get("/download", async (req, res) => {
  const videoUrl = req.query.url;
  const type = req.query.type || "audio";

  if (!videoUrl || !ytdl.validateURL(videoUrl)) {
    return res.status(400).json({ error: "Invalid YouTube URL." });
  }

  try {
    const info = await ytdl.getInfo(videoUrl);
    const title = info.videoDetails.title.replace(/[^a-zA-Z0-9]/g, "_");

    res.header(
      "Content-Disposition",
      `attachment; filename="${title}.${type === "video" ? "mp4" : "mp3"}"`
    );

    if (type === "video") {
      ytdl(videoUrl, { quality: "highestvideo" }).pipe(res);
    } else {
      ytdl(videoUrl, { filter: "audioonly", quality: "highestaudio" }).pipe(res);
    }
  } catch (err) {
    res.status(500).json({ error: "Download failed." });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server is running on port ${PORT}`);
});
