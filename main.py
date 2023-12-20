
from fastapi import FastAPI, HTTPException
from pytube import YouTube
import logging
import time

app = FastAPI()

logging.basicConfig(level=logging.ERROR)

# Rate limiter variables
MIN_REQUEST_INTERVAL = 2  # Minimum time between requests in seconds
last_request_time = 0

@app.get("/download/")
async def download_video(link: str):
    global last_request_time

    try:
        # Rate limiting
        current_time = time.time()
        elapsed_time = current_time - last_request_time
        if elapsed_time < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed_time)

        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url

        # Update last request time
        last_request_time = time.time()

        return {"download_link": download_url}
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
