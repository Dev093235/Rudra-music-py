from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
import logging

app = Flask(__name__)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "🎵 Rudra Music API with Cookies is running!"

@app.route('/audio')
def get_audio():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing search query `q`"}), 400

    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("/tmp", filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filepath,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',  # Make sure this file exists in your root
        'logger': app.logger,
        'quiet': False,
        'verbose': True,
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
            elif not info:
                return jsonify({"error": "No video found"}), 404
    except yt_dlp.utils.DownloadError as e:
        app.logger.error(f"yt-dlp error: {str(e)}")
        return jsonify({"error": "DownloadError", "detail": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({"error": "Unhandled exception", "detail": str(e)}), 500

    if not os.path.exists(filepath):
        return jsonify({"error": "Audio file not created - check ffmpeg and permission"}), 500

    return send_file(
        filepath,
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name=f"{query.replace(' ', '_')}.mp3"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
