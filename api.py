import uvicorn
from fastapi import FastAPI, status, Depends, HTTPException
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import engine
import models
import schemas
from auth import get_current_user, create_access_token, get_db
from datetime import timedelta
import crud as crud_bd
from passlib.context import CryptContext

# função pra iniciar a conexao com o banco de dados
def init_db():
  Base.metadata.create_all(bind=engine)


ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title='Nossa APi', on_startup=[init_db])

def get_db():
  db = SessionLocal()
  try: 
    yield db
  finally: 
    db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/token", response_model=schemas.user.Token, tags=["Users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_bd.get_user(db, username=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.user.UserResponse, tags=["Users"])
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    return crud_bd.create_user(db, user)

@app.get("/users/me/", response_model=schemas.user.UserResponse, tags=["Users"])
def read_users_me(current_user: schemas.user.UserResponse = Depends(get_current_user)):
    return current_user


# Endpoint pra trazer todos os items
@app.get('/api/items', response_model=list[schemas.item.ItemSchema], status_code=status.HTTP_200_OK, tags=["Items CRUD"], description="descrição do endpoint", name="nome da função ou endpoint")
def getAll(db: Session = Depends(get_db)):
    return crud_bd.get_items(db)

@app.get("/items/{item_id}", response_model=schemas.item.ItemSchema, tags=["Items CRUD"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_bd.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item


@app.post('/api/items', status_code=status.HTTP_201_CREATED, tags=["Items CRUD"], response_model=schemas.item.ItemSchema)
def postItem(item: schemas.item.ItemSchema, db: Session = Depends(get_db)):
  try: 
    return crud_bd.create_item(db, item)
  except Exception as e: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/items/{item_id}", response_model=schemas.item.ItemSchema, tags=["Items CRUD"])
def update_item(item_id: int, item: schemas.item.ItemSchema, db: Session = Depends(get_db), current_user: schemas.user.UserResponse  = Depends(get_current_user)):
    db_item = crud_bd.update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.item.ItemSchema, tags=["Items CRUD"])
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: schemas.user.UserResponse  = Depends(get_current_user)):
    db_item = crud_bd.delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"Item deletado com sucesso"}




# @app.get('/api/items', response_model=list[schemas.item.ItemSchema], status_code=status.HTTP_200_OK, tags=["Items CRUD"], description="descrição do endpoint", name="nome da função ou endpoint")
# async def getAll(db: AsyncSession = Depends(get_db)):
#     return await crud_bd.get_items(db)



# @app.post('/api/items',  status_code=status.HTTP_201_CREATED, tags=["Items CRUD"], response_model=list[schemas.item.ItemSchema])
# async def postItem(item: schemas.item.ItemSchema, db: AsyncSession = Depends(get_db)):
#   return await crud_bd.create_item(db, item)





# Endport para trazer o item de acordo com o ID
# @app.get('/api/items/{itemId}', status_code=status.HTTP_200_OK, tags=["Items CRUD"])
# def getById(itemId: int)->Item:
#   for item in items:
#     if item['id'] == itemId:
#       return item


# # Endpoint pra criar um item
# @app.post('/api/items', status_code=status.HTTP_201_CREATED, tags=["Items CRUD"])
# def postItem(item: Item) -> Item:
#   item['id'] = len(items) + 1
#   items.append(item)
#   return item

# @app.put('/api/items/{itemId}', status_code=status.HTTP_200_OK,tags=["Items CRUD"])
# def putItem(itemId: int, dataItem:Item) -> Item:
#   for index, item in enumerate(items):
#     if item['id'] == itemId:
#       items[index] = dataItem
#       return dataItem
#   return {
#     "erro": "Item não foi encontrato"
#   }

# @app.delete('/api/items/{itemId}', status_code=status.HTTP_202_ACCEPTED, tags=["Items CRUD"])
# def deleteItem(itemId: int)-> Item:
#   for index, item in enumerate(items):
#     if item['id'] == itemId:
#       items.pop(index)
#       return {"sucess": "Seu item foi deletado"}
#   return {
#     "erro": "Item não foi encontrato"
#   }





if __name__ == '__main__':
  uvicorn.run(app, port=8000)

  # https://www.youtube.com/watch?v=9vRpj0RbkBg