from fastapi import FastAPI
from rtp.app.routes import router

app = FastAPI(title="Real-Time Decision Pipeline")

app.include_router(router)


@app.get("/")
def health():
    return {"status": "ok"}
