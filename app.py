from flask import Flask, request, send_file, jsonify
from pytube import Search, YouTube
import os
import uuid

app = Flask(__name__)

@app.route('/audio')
def download_audio():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    try:
        search = Search(query)
        video = search.results[0]
        yt = YouTube(video.watch_url)
        stream = yt.streams.filter(only_audio=True).first()

        filename = f"{uuid.uuid4()}.mp3"
        path = stream.download(filename=filename)

        return send_file(
            path,
            as_attachment=True,
            download_name=f"{query}.mp3",
            mimetype="audio/mpeg"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True)
