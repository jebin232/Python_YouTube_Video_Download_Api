from flask import Flask, request, jsonify
from pytube import YouTube
import time

app = Flask(__name__)

@app.route('/download/', methods=['POST'])
def download_video():
    try:
        data = request.json
        if not data or 'link' not in data:
            return jsonify({"detail": "No link provided"}), 400

        yt = YouTube(data['link'])
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return jsonify({"download_link": download_url})
    except Exception as e:
        if "HTTP Error 429" in str(e):
            print("Rate limit exceeded. Waiting before retrying...")
            time.sleep(10)  # Wait for 60 seconds before retrying
            return download_video()  # Retry the request
        else:
            return jsonify({"detail": "Failed to process the video link."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
