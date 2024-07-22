********************************** database.py *********************************************

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'postgresql+asyncpg://postgres.firiyxuzrdddccskefdp:IwPbHINHLksJmGSE@aws-0-us-east-1.pooler.supabase.com:6543/postgres'

engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"prepared_statement_cache_size": 0})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

********************************** squemas.py *********************************************


from pydantic import BaseModel

class ItemSchema(BaseModel):
  id: int
  name: str

********************************** models.py *********************************************


from database import Base
from sqlalchemy import Column, Integer, String

class ItemModel(Base):
  __tablename__ = 'items'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)

********************************** crud_bd.py *********************************************

from models import ItemModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_items(db: AsyncSession):
  result = await db.execute(select(ItemModel))

  return result.scalars().all()

********************************** api.py *********************************************


import uvicorn
from fastapi import FastAPI, status, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schemas
import crud_bd

# função pra iniciar a conexao com o banco de dados
async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title='Nossa APi', on_startup=[init_db])

async def get_db():
  async with SessionLocal() as db:
    yield db

# Endpoint pra trazer todos os items
@app.get('/api/items', response_model=list[schemas.ItemSchema], status_code=status.HTTP_200_OK, tags=["Items CRUD"], description="descrição do endpoint", name="nome da função ou endpoint")
async def getAll(db: AsyncSession = Depends(get_db)):
    return await crud_bd.get_items(db)




## com SQLITE



********************************** database.py *********************************************

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///C:/Users/diego/OneDrive/Documentos/Projetos/testes/bd.db'

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


********************************** squemas.py *********************************************


from pydantic import BaseModel

class ItemSchema(BaseModel):
  id: int
  name: str

********************************** models.py *********************************************


from database import Base
from sqlalchemy import Column, Integer, String

class ItemModel(Base):
  __tablename__ = 'items'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)


********************************** crud_bd.py *********************************************

from models import ItemModel
from sqlalchemy.orm import Session
from sqlalchemy import select

async def get_items(db: Session):
  result = db.execute(select(ItemModel))
  return result.scalars().all()

********************************** api.py *********************************************


import uvicorn
from fastapi import FastAPI, status, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
import models
import schemas
import crud_bd

# função pra iniciar a conexao com o banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title='Nossa APi', on_startup=[init_db])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint pra trazer todos os items
@app.get('/api/items', response_model=list[schemas.ItemSchema], status_code=status.HTTP_200_OK, tags=["Items CRUD"], description="descrição do endpoint", name="nome da função ou endpoint")
async def getAll(db: Session = Depends(get_db)):
    return await crud_bd.get_items(db)
