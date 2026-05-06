from fastapi import FastAPI

from app.api.routes import api_router

app = FastAPI(
    title="Contacts API",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
