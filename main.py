from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

from starlette.middleware.cors import CORSMiddleware
import mangum

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    
)



app.include_router(router, prefix="/api")

app.mount("/", StaticFiles(directory="app/frontend/src", html=True), name="frontend")


app.include_router(router, prefix="/api")

handler = mangum.Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000)

