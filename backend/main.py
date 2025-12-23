# main.py
from fastapi import FastAPI

from core.lifespan import lifespan
from auth.google import router as google_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

# include auth routes


app.include_router(google_router)
origins = [
    "http://localhost:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "ok"}
