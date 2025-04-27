from pydantic import BaseModel
from typing import Optional
from datetime import date

class Produto(BaseModel):
    id: Optional[int]
    nome: str
    categoria: str
    validade: Optional[date]

class Compra(BaseModel):
    id: Optional[int]
    produto_id: int
    data_compra: date
    mercado: str
    valor: float
    quantidade: int

class Uso(BaseModel):
    id: Optional[int]
    produto_id: int
    data_uso: date
    quantidade: int
