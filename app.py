from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return "🎵 Rudra Music API is running!"

@app.route('/audio')
def get_audio():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing search query `q`"}), 400

    # Generate a unique filename
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
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            if 'entries' in info:
                info = info['entries'][0]
    except Exception as e:
        return jsonify({"error": "Download failed", "detail": str(e)}), 500

    if not os.path.exists(filepath):
        return jsonify({"error": "Audio file not created"}), 500

    return send_file(
        filepath,
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name=f"{query.replace(' ', '_')}.mp3"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
