from fastapi import FastAPI

app = FastAPI(
    title="AI Receptionist",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "AI Receptionist",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}