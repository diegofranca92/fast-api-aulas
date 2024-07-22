import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, status


app = FastAPI(title='Nossa APi')

class OutroTipo(BaseModel):
  name: str

class Item(BaseModel):
  id: int
  name: str
  outro_tipo: OutroTipo

# Criação de uma lista de items
items:list[Item] = [
  {
    "id": 1,
    "name": 'Item 1'
  }
]



# Endpoint pra trazer todos os items
@app.get('/api/items', status_code=status.HTTP_200_OK, tags=["Items CRUD"], description="descrição do endpoint", name="nome da função ou endpoint")
def getAll()->list[Item]:
    return items

# Endport para trazer o item de acordo com o ID
@app.get('/api/items/{itemId}', status_code=status.HTTP_200_OK, tags=["Items CRUD"])
def getById(itemId: int)->Item:
  for item in items:
    if item['id'] == itemId:
      return item


# Endpoint pra criar um item
@app.post('/api/items', status_code=status.HTTP_201_CREATED, tags=["Items CRUD"])
def postItem(item: Item) -> Item:
  item['id'] = len(items) + 1
  items.append(item)
  return item

@app.put('/api/items/{itemId}', status_code=status.HTTP_200_OK,tags=["Items CRUD"])
def putItem(itemId: int, dataItem:Item) -> Item:
  for index, item in enumerate(items):
    if item['id'] == itemId:
      items[index] = dataItem
      return dataItem
  return {
    "erro": "Item não foi encontrato"
  }

@app.delete('/api/items/{itemId}', status_code=status.HTTP_202_ACCEPTED, tags=["Items CRUD"])
def deleteItem(itemId: int)-> Item:
  for index, item in enumerate(items):
    if item['id'] == itemId:
      items.pop(index)
      return {"sucess": "Seu item foi deletado"}
  return {
    "erro": "Item não foi encontrato"
  }





if __name__ == '__main__':
  uvicorn.run(app, port=8000)

  # https://www.youtube.com/watch?v=9vRpj0RbkBg