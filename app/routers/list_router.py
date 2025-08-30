from fastapi import APIRouter,Depends ,HTTPException
from sqlalchemy.orm import Session
from typing import List as ListType
from app.db.database import get_db
from app.schemas import list as list_schema
from app.crud import list_crud

router = APIRouter(prefix="/lists" , tags=["lists"])

@router.get("/" , response_model= ListType[list_schema.List])
def read_lists (db: Session = Depends(get_db)):
    return list_crud.get_lists(db)

@router.post("/" , response_model=list_schema.List)
def create_list(list_in : list_schema.ListCreate , db:Session = Depends(get_db)):
    return list_crud.create_list(db, list_in)

@router.delete("/{list_id}" , response_model=list_schema.List)
def remove_list(list_id: int , db:Session = Depends(get_db)):
    db_list = list_crud.delete_list(db , list_id)
    if not db_list:
        raise HTTPException(status_code=404 , detail="List not found")
    return db_list

@router.post("/{list_id}/card" , response_model=list_schema.Card)
def add_card(list_id: int , card_in: list_schema.CardCreate, db : Session = Depends(get_db)):
    return list_crud.add_card(db , list_id , card_in)

@router.delete("/{list_id}/cards/{card_id}" , response_model=list_schema.Card)
def remove_card(list_id: int , card_id : int , db:Session = Depends(get_db)):
    db_card = list_crud.delete_card(db , list_id , card_id)
    if not db_card:
        raise HTTPException(status_code=404 , detail="Card not found")
    return db_card
