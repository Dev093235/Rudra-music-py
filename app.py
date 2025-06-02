Rudra YouTube MP3 Downloader API - Render Ready

from flask import Flask, request, send_file, jsonify import yt_dlp import os import uuid

app = Flask(name)

@app.route('/') def home(): return "\U0001F3B5 Rudra YouTube MP3 API is Live! Use /audio?q=your+song"

@app.route('/audio') def download_audio(): query = request.args.get('q') if not query: return jsonify({"error": "Missing ?q=song name"}), 400

filename = f"{uuid.uuid4().hex}.mp3"
filepath = os.path.join("/tmp", filename)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': filepath,
    'noplaylist': True,
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        if 'entries' in info:
            info = info['entries'][0]
        else:
            return jsonify({"error": "No results found"}), 404
except Exception as e:
    return jsonify({"error": "Download failed", "detail": str(e)}), 500

if not os.path.exists(filepath):
    return jsonify({"error": "MP3 file not found after download"}), 500

return send_file(filepath, mimetype='audio/mpeg', as_attachment=True, download_name=f"{query}.mp3")

if name == 'main': app.run(host='0.0.0.0', port=10000)

