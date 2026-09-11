from fastapi import FastAPI

from app.routes.receptionist import router as receptionist_router

app = FastAPI(
    title="AI Receptionist",
    version="0.1.0",
)

app.include_router(receptionist_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "AI Receptionist",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}