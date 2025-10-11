from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.card import Card
from app.models.list import List
from app.models.board import Board
from app.auth.dependencies import get_current_user
from app.utils.send_email import send_email
from typing import List as TypingList
from pydantic import BaseModel

router = APIRouter()

class MemberAssignment(BaseModel):
    user_id: int

class MemberResponse(BaseModel):
    id: int
    username: str
    email: str

@router.post("/cards/{card_id}/members")
async def add_member_to_card(
    card_id: int,
    member_data: MemberAssignment,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a member to a card and send email notification"""
    
    # Get the card
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Get the list and board to check permissions
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Check if current user has permission (board owner or admin)
    if board.owner_id != current_user.id and current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized to add members")
    
    # Get the user to be added as member
    member_user = db.query(User).filter(User.id == member_data.user_id).first()
    if not member_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is already a member
    if member_user.id in (card.members or []):
        raise HTTPException(status_code=400, detail="User is already a member of this card")
    
    # Add member to card
    if card.members is None:
        card.members = []
    card.members.append(member_user.id)
    
    try:
        db.commit()
        db.refresh(card)
        
        # Send email notification
        email_subject = f"You've been added to a card: {card.text}"
        email_body = f"""
Hello {member_user.username},

You have been added to a card in the board "{board.title}".

Card Details:
- Card: {card.text}
- Board: {board.title}
- Added by: {current_user.username}

You can now view and collaborate on this card.

Best regards,
Task Management System
        """
        
        if member_user.email:
            try:
                send_email(member_user.email, email_subject, email_body)
            except Exception as e:
                print(f"Failed to send email to {member_user.email}: {e}")
                # Don't fail the request if email fails
        
        return {"message": "Member added successfully", "member": {
            "id": member_user.id,
            "username": member_user.username,
            "email": member_user.email
        }}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add member: {str(e)}")

@router.delete("/cards/{card_id}/members/{user_id}")
async def remove_member_from_card(
    card_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a member from a card"""
    
    # Get the card
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Get the list and board to check permissions
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Check if current user has permission (board owner or admin)
    if board.owner_id != current_user.id and current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized to remove members")
    
    # Remove member from card
    if card.members and user_id in card.members:
        card.members.remove(user_id)
        
        try:
            db.commit()
            return {"message": "Member removed successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to remove member: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="User is not a member of this card")

@router.get("/cards/{card_id}/members")
async def get_card_members(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all members of a card"""
    
    # Get the card
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Get the list and board to check permissions
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Check if current user has permission to view board
    if board.owner_id != current_user.id and current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized to view members")
    
    # Get member details
    members = []
    if card.members:
        for member_id in card.members:
            user = db.query(User).filter(User.id == member_id).first()
            if user:
                members.append({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                })
    
    return {"members": members}

@router.get("/boards/{board_id}/available-members")
async def get_available_members(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users that can be added as members to cards in this board"""
    
    # Get the board
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Check if current user has permission
    if board.owner_id != current_user.id and current_user.role not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized to view available members")
    
    # Get all users (in a real app, you might want to limit this to board members)
    users = db.query(User).all()
    
    available_members = []
    for user in users:
        available_members.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    
    return {"available_members": available_members}


