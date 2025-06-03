const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => {
  res.send('🎵 Rudra MP3 API is Live! Use /song?q=your+song+name');
});

app.get('/song', async (req, res) => {
  const query = req.query.q;
  if (!query) return res.status(400).json({ error: 'Missing ?q=song name' });

  try {
    const search = await axios.get(`https://saavn.dev/api/search/songs?query=${encodeURIComponent(query)}`);
    const song = search.data.data.results[0];
    if (!song) return res.status(404).json({ error: 'No song found' });

    const songId = song.id;
    const songDetails = await axios.get(`https://saavn.dev/api/songs/${songId}`);
    const mp3Url = songDetails.data.data[0].downloadUrl.find(x => x.quality === '320kbps').link;

    res.redirect(mp3Url); // Direct play/download
  } catch (err) {
    res.status(500).json({ error: 'Something went wrong', detail: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`🎧 Server running on port ${PORT}`);
});
