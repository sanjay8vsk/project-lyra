from fastapi import FastAPI  # type: ignore
from app.routes.upload import router as upload_router  # type: ignore
from app.routes.chat import router as chat_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Lyra backend running successfully"}