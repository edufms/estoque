from pydantic import BaseModel
from typing import Optional
from datetime import date

class Produto(BaseModel):
    def __init__(self, id=None, nome=None, categoria=None, validade=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.validade = validade

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
