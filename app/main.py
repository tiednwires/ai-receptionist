"""Create and configure the FastAPI application."""

# FastAPI is the web framework used to define the API application and routes.
from fastapi import FastAPI

# Import the receptionist router under a descriptive local name. Keeping the
# route definitions in another module prevents this entry point from growing
# into one large file as the project expands.
from app.routes.receptionist import router as receptionist_router

# Create the main application object that Uvicorn imports and serves.
# The title and version appear in the generated OpenAPI documentation.
app = FastAPI(
    title="AI Receptionist",
    version="0.1.0",
)

# Register every endpoint defined by the receptionist router with this app.
app.include_router(receptionist_router)


@app.get("/")
def root():
    """Return a small response showing that the API is reachable."""

    return {
        "status": "ok",
        "service": "AI Receptionist",
    }


@app.get("/health")
def health():
    """Return a simple health response for local checks and monitoring."""

    return {"status": "healthy"}
