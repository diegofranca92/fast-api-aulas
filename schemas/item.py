from pydantic import BaseModel, Field, constr, validator
from typing import Optional

class ItemSchema(BaseModel):
  name: constr(min_length=3, max_length=50) = Field(..., description="Nome não pode ser vazio e tem que ter o comprimento de 3 a 50 cacteres")
  description: Optional[constr(min_length=10, max_length=200)] = Field(..., description="Nome não pode ser vazio e tem que ter o comprimento de 3 a 50 cacteres")
  

  @validator('name', always=True)
  def validate_name(cls, value):
    if len(value) > 10:
      raise ValueError('Ele é alemão')
    return value
 
  class Config:
    orm_mode = True