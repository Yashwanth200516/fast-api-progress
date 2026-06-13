from pydantic import BaseModel

class Students(BaseModel):
    name:str
    age:int
    branch:str
    usn:str
    phone_no:str
    address:str