from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..schemas import MediaType, ItemStatus, ItemCreate
from ..models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/")
async def add_item():
    pass

@router.get("/")
async def get_items():
    pass

@router.get("/{item_id}")
async def get_item():
    pass

@router.patch("/{item_id}")
async def update_item():
    pass

@router.delete("/{item_id}")
async def delete_item():
    pass