from fastapi import FastAPI, HTTPException
from pytube import YouTube

app = FastAPI()

@app.get("/download/")
async def download_video(link: str):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        download_url = stream.url
        return {"download_link": download_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
