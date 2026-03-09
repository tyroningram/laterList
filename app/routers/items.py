from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import MediaType, ItemStatus, ItemCreate, ItemResponse, ItemUpdate
from ..models import Item
from .auth import get_current_user

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/", response_model=ItemResponse)
async def add_item(item: ItemCreate, user: user_dependency, db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    new_item = Item(**item.model_dump(mode="json"), user_id=user.get("id"))
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[ItemResponse])
async def get_items(user: user_dependency, media_type: MediaType | None = None, status: ItemStatus | None = None, title: str | None = None, limit: int = 10, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    query = db.query(Item)
    if media_type is not None:
        query = query.filter(Item.media_type == media_type.value)
    if status is not None:
        query = query.filter(Item.status == status.value)
    if title is not None:
        query = query.filter(Item.title.ilike(f"%{title}%"))

    return query.filter(Item.user_id == user.get("id")).limit(limit).all()


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(user: user_dependency, item_id: int, db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    db_item = db.query(Item).filter(Item.id == item_id).filter(Item.user_id == user.get("id")).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    return db_item

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(user: user_dependency, item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    db_item = db.query(Item).filter(Item.id == item_id).filter(Item.user_id == user.get("id")).first()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found.")

    update_data = item.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(user: user_dependency, item_id: int, db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    db_item = db.query(Item).filter(Item.id == item_id).filter(Item.user_id == user.get("id")).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    db.delete(db_item)
    db.commit()
    return 