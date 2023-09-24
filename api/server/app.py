from fastapi import FastAPI
from .routes.contact import router as ContactRouter
app = FastAPI()


app.include_router(ContactRouter, tags=["Contact"], prefix="/contact")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome"}
