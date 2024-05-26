from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/download/', methods=['POST'])
def download_video():
    try:
        data = request.json
        if not data or 'link' not in data:
            print(f"Received data: {data}")  # Logging received data
            return jsonify({"detail": "No link provided"}), 400

        yt = YouTube(data['link'])
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return jsonify({"download_link": download_url})
    except Exception as e:
        print(f"Error: {e}")  # Logging error
        return jsonify({"detail": "Failed to process the video link.{e}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
