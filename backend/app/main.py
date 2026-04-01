# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.startup import on_startup

app = FastAPI(
    title="Real Estate AI Search",
    version="1.0.0"
)

# Enable CORS for frontend integration
# NOTE: Cannot use allow_origins=["*"] with allow_credentials=True
# So we explicitly list frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Create React App default
        "http://localhost:5173",      # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,          # Changed to False to allow any origin in list
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup():
    on_startup()