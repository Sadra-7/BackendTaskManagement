#!/usr/bin/env python3
"""
Board duplication utility
"""

from sqlalchemy.orm import Session
from app.models.board import Board
from app.models.list import List
from app.models.card import Card
from app.models.user import User

def duplicate_board_for_user(db: Session, original_board_id: int, new_user_id: int) -> int:
    """
    Duplicate a board with all its lists and cards for a new user
    
    Args:
        db: Database session
        original_board_id: ID of the board to duplicate
        new_user_id: ID of the user who will own the new board
    
    Returns:
        ID of the newly created board
    """
    try:
        # Get the original board
        original_board = db.query(Board).filter(Board.id == original_board_id).first()
        if not original_board:
            raise ValueError(f"Board {original_board_id} not found")
        
        # Create new board for the user
        new_board = Board(
            title=f"{original_board.title} (Copy)",
            owner_id=new_user_id,
            workspace_id=original_board.workspace_id
        )
        db.add(new_board)
        db.flush()  # Get the new board ID
        
        # Get all lists from the original board
        original_lists = db.query(List).filter(List.board_id == original_board_id).all()
        
        # Duplicate each list
        for original_list in original_lists:
            new_list = List(
                title=original_list.title,
                board_id=new_board.id,
                user_id=new_user_id,
                color=original_list.color
            )
            db.add(new_list)
            db.flush()  # Get the new list ID
            
            # Get all cards from the original list
            original_cards = db.query(Card).filter(Card.list_id == original_list.id).all()
            
            # Duplicate each card
            for original_card in original_cards:
                new_card = Card(
                    text=original_card.text,
                    position=original_card.position,
                    list_id=new_list.id,
                    start_date=original_card.start_date,
                    end_date=original_card.end_date,
                    description=original_card.description,
                    comments=original_card.comments,
                    members=original_card.members  # Copy members if any
                )
                db.add(new_card)
        
        db.commit()
        print(f"✅ Board duplicated successfully! New board ID: {new_board.id}")
        return new_board.id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Failed to duplicate board: {e}")
        raise e

def get_board_data(db: Session, board_id: int) -> dict:
    """
    Get complete board data including lists and cards
    
    Args:
        db: Database session
        board_id: ID of the board
    
    Returns:
        Dictionary containing board data
    """
    try:
        # Get board
        board = db.query(Board).filter(Board.id == board_id).first()
        if not board:
            raise ValueError(f"Board {board_id} not found")
        
        # Get lists
        lists = db.query(List).filter(List.board_id == board_id).all()
        
        # Get cards for each list
        board_data = {
            "board": {
                "id": board.id,
                "title": board.title,
                "owner_id": board.owner_id,
                "workspace_id": board.workspace_id
            },
            "lists": []
        }
        
        for list_item in lists:
            cards = db.query(Card).filter(Card.list_id == list_item.id).all()
            
            list_data = {
                "id": list_item.id,
                "title": list_item.title,
                "board_id": list_item.board_id,
                "user_id": list_item.user_id,
                "color": list_item.color,
                "cards": []
            }
            
            for card in cards:
                card_data = {
                    "id": card.id,
                    "text": card.text,
                    "position": card.position,
                    "list_id": card.list_id,
                    "start_date": card.start_date,
                    "end_date": card.end_date,
                    "description": card.description,
                    "comments": card.comments,
                    "members": card.members
                }
                list_data["cards"].append(card_data)
            
            board_data["lists"].append(list_data)
        
        return board_data
        
    except Exception as e:
        print(f"❌ Failed to get board data: {e}")
        raise e
