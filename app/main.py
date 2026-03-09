from fastapi import FastAPI

from .database import Base, engine
from .routers.items import router as items_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(items_router)

@app.get("/")
async def health():
    return {"health": "ok"}

