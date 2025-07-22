from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI()

app.include_router(router, prefix="/api")

app.mount("/", StaticFiles(directory="app/frontend/src", html=True), name="frontend")


app.include_router(router, prefix="/api")
