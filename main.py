from fastapi import FastAPI, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiterDependency
from pytube import YouTube
import logging

app = FastAPI()

logging.basicConfig(level=logging.ERROR)

# Configure rate limiting
limiter = FastAPILimiter(app, key_func=lambda _: "global", block=True)
rate_limiter = RateLimiterDependency(limiter)

@app.get("/download/")
@limiter.limit("5/minute")  # Adjust the rate limit as needed
async def download_video(link: str, rate_limit: bool = Depends(rate_limiter)):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return {"download_link": download_url}
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
