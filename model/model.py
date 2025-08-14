from typing import Optional

from pydantic import BaseModel



class login_detail(BaseModel):
    admin_name:str
    admin_pass:str
class Cargo(BaseModel):
    cargo_name:str
    description: Optional[str] = None
    quantity:int
    archive:bool

class cargo_ud(BaseModel):
    cargo_id:str
    cargo_name: str
    description: Optional[str] = None
    quantity: int
    archive: bool

class cargo_dl(BaseModel):
    cargo_id: str


class CargoItem(BaseModel):
    cargo_name: str
    description:str
class read_cargo(BaseModel):
    page:int
    rec_size:int
    filter: CargoItem
    sort:str

class arranged_cargo_names(BaseModel):
    enter_descending_or_ascending:str

class arranged_cargo_quantity(BaseModel):
    enter_descending_or_ascending:str


class gen_tock(BaseModel):
    cargo_name:str






