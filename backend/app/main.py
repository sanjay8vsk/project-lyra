from fastapi import FastAPI  # type: ignore
from app.routes.upload import router as upload_router  # type: ignore
from app.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Lyra backend running successfully"}