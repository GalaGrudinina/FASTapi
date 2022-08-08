from pydantic import BaseModel

class Vessel(BaseModel):
    name:str
    id:str
    naccsCode:str
    date:str
    destination:str



    