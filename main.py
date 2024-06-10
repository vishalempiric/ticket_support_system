from fastapi import FastAPI
from src.routers.email_router import email_router

app = FastAPI()

# Include your email router in the app
app.include_router(email_router, prefix="/api", tags=["Email"])

