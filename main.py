from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from pytube import YouTube

app = FastAPI()

class VideoLink(BaseModel):
    link: str

@app.post("/download/")
def download_video(video: VideoLink):
    try:
        yt = YouTube(video.link)
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return {"download_link": download_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process the video link.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
