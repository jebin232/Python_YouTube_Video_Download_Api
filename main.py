from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    if 'link' not in data:
        return jsonify({"detail": "No link provided"}), 400

    try:
        yt = YouTube(data['link'])
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return jsonify({"download_link": download_url})
    except Exception as e:
        return jsonify({"detail": "Failed to process the video link."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
