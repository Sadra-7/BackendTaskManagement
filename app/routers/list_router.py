from fastapi import APIRouter,Depends ,HTTPException , Body
from sqlalchemy.orm import Session
from typing import List as ListType
from app.db.database import get_db
from app.schemas import list as list_schema
from app.crud import list_crud
from app.routers.users import get_current_user
from app.models.user import User

router = APIRouter(prefix="/lists" , tags=["lists"])

@router.get("/" , response_model= ListType[list_schema.List])
def read_lists (db: Session = Depends(get_db) , current_user: User = Depends(get_current_user)):
    return list_crud.get_lists(db , user_id=current_user.id)

@router.post("/" , response_model=list_schema.List)
def create_list(list_in : list_schema.ListCreate , db:Session = Depends(get_db) , current_user: User = Depends(get_current_user)):
    return list_crud.create_list(db, list_in , user_id=current_user.id)

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

@router.patch("/{list_id}/color" , response_model=list_schema.List)
def update_list_color(list_id : int , color_update : dict = Body(...) , db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    color = color_update.get("color")
    if not color:
        raise HTTPException(status_code=400 , detail="Color is required")
    
    db_list = list_crud.updat_color_list(db , list_id = list_id , color=color , user_id=current_user.id)
    if not db_list:
        raise HTTPException(status_code=404 , detail="List not found")
    return db_list

@router.patch("/{list_id}" , response_model=list_schema.List)
def update_list(list_id : int , list_update: list_schema.ListUpdate , db: Session = Depends(get_db) , current_user : User = Depends(get_current_user)):
    db_list = list_crud.update_list(db , list_id = list_id , user_id = current_user.id , title = list_update.title , color = list_update.color)
    if not db_list:
        raise HTTPException(status_code=404 , detail="List not found")
    return db_list 

@router.post("/{list_id}/card", response_model=list_schema.Card)
def add_card(list_id: int, card_in: list_schema.CardCreate, db: Session = Depends(get_db)):
    return list_crud.add_card(db, list_id, card_in)

@router.delete("/{list_id}/cards/{card_id}", response_model=list_schema.Card)
def remove_card(list_id: int, card_id: int, db: Session = Depends(get_db)):
    db_card = list_crud.delete_card(db, list_id, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.patch("/{list_id}/cards/{card_id}", response_model=list_schema.Card)
def update_card(list_id: int, card_id: int, card_update: list_schema.CardUpdate, db: Session = Depends(get_db)):
    db_card = list_crud.update_card(db, list_id, card_id, card_update.text)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card