from flask import Flask, request, jsonify, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "🎵 Rudra Flask Audio API is running!"

@app.route('/audio')
def get_audio():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1:',
        'skip_download': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            if 'entries' in result:
                result = result['entries'][0]

            audio_url = result['url']
            return redirect(audio_url)
    except Exception as e:
        return jsonify({"error": "Failed to fetch audio", "detail": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
