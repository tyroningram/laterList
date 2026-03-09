from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import MediaType, ItemStatus, ItemCreate, ItemResponse, ItemUpdate
from ..models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/", response_model=ItemResponse)
async def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(**item.model_dump(mode="json"))
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[ItemResponse])
async def get_items(media_type: MediaType | None = None, status: ItemStatus | None = None, title: str | None = None, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Item)

    if media_type is not None:
        query = query.filter(Item.media_type == media_type.value)
    if status is not None:
        query = query.filter(Item.status == status.value)
    if title is not None:
        query = query.filter(Item.title.ilike(f"%{title}%"))

    return query.limit(limit).all()


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NO_CONTENT, detail="Item not found.")
    return db_item

@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):

    db_item  = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    
    for field, value in item.model_dump(mode="json").items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NO_CONTENT, detail="Item not found.")
    db.delete(db_item)
    db.commit()
    return status.HTTP_204_NO_CONTENT