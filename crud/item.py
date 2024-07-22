from models import ItemModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.item import ItemSchema

def get_items(db: Session):
  # result = db.execute(select(ItemModel).offset(skip).limit(limit))
  result = db.execute(select(ItemModel))

  return result.scalars().all()

def get_item(db: Session, item_id: int):
    return db.query(ItemModel).filter(ItemModel.id == item_id).first()

def create_item(db: Session, item: ItemSchema):
  db_item = ItemModel(**item.dict())
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

def update_item(db: Session, item_id: int, item: ItemSchema):
  db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
  if db_item:
      for key, value in item.dict().items():
          setattr(db_item, key, value)
      db.commit()
      db.refresh(db_item)
      return db_item
  return None

def delete_item(db: Session, item_id: int):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
