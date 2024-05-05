from fastapi import FastAPI, HTTPException, Depends
from pytube import YouTube
from fastapi_limiter import FastAPILimiter

app = FastAPI()

# Configure rate limiting (for example, limit to 5 requests per minute)
limiter = FastAPILimiter(key="ip", default_limits=["5/minute"])

@app.get("/download/")
@limiter.limit("5/minute")
def download_video(link: str):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return {"download_link": download_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process the video link.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
