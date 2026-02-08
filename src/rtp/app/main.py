from fastapi import FastAPI

app = FastAPI(title="Real-Time Decision Pipeline")


@app.get("/")
def health():
    return {"status": "ok"}

