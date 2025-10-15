# app/routers/boards.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from app.db.database import get_db
from app.models.board import Board
from app.models.invitation import BoardMember
from app.schemas.board import BoardCreate, BoardUpdate, Board as BoardSchema
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/boards", tags=["Boards"])

def has_board_access(db: Session, user_id: int, board_id: int) -> bool:
    """
    Check if user has access to a board (either as owner or member)
    """
    # Check if user is owner
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == user_id).first()
    if board:
        return True
    
    # Check if user is a member
    member = db.query(BoardMember).filter(
        BoardMember.board_id == board_id,
        BoardMember.user_id == user_id
    ).first()
    
    return member is not None

# -----------------------
# دریافت بردها بر اساس ورک‌اسپیس
# -----------------------
@router.get("/", response_model=List[BoardSchema])
def get_boards(
    workspace_id: int = Query(None, description="شناسه ورک‌اسپیس برای فیلتر بردها (اختیاری)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت همه بردهای متعلق به کاربر
    شامل بردهایی که کاربر مالک آن‌هاست و بردهایی که کاربر عضو آن‌هاست
    """
    # Get boards where user is owner
    owned_query = db.query(Board).filter(Board.owner_id == current_user.id)
    if workspace_id is not None:
        owned_query = owned_query.filter(Board.workspace_id == workspace_id)
    owned_boards = owned_query.all()
    
    # Get boards where user is a member (through invitations)
    member_query = (
        db.query(Board)
        .join(BoardMember, Board.id == BoardMember.board_id)
        .filter(BoardMember.user_id == current_user.id)
    )
    if workspace_id is not None:
        member_query = member_query.filter(Board.workspace_id == workspace_id)
    member_boards = member_query.all()
    
    # Combine both lists and remove duplicates
    all_boards = owned_boards + member_boards
    unique_boards = []
    seen_ids = set()
    
    for board in all_boards:
        if board.id not in seen_ids:
            unique_boards.append(board)
            seen_ids.add(board.id)
    
    return unique_boards

# Simple boards endpoint without workspace filtering
@router.get("/all")
def get_all_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all boards a user has access to (owned or member)
    """
    # Get boards where user is owner
    owned_boards = db.query(Board).filter(Board.owner_id == current_user.id).all()
    
    # Get boards where user is a member
    member_boards = (
        db.query(Board)
        .join(BoardMember, Board.id == BoardMember.board_id)
        .filter(BoardMember.user_id == current_user.id)
        .all()
    )
    
    # Combine and deduplicate
    all_boards = owned_boards + member_boards
    unique_boards = []
    seen_ids = set()
    
    for board in all_boards:
        if board.id not in seen_ids:
            unique_boards.append(board)
            seen_ids.add(board.id)
    
    return unique_boards

# Debug endpoint to check user's board access
@router.get("/debug/my-boards")
def debug_my_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Debug endpoint to see all boards a user has access to
    """
    # Get boards where user is owner
    owned_boards = db.query(Board).filter(Board.owner_id == current_user.id).all()
    
    # Get boards where user is a member
    member_boards = (
        db.query(Board)
        .join(BoardMember, Board.id == BoardMember.board_id)
        .filter(BoardMember.user_id == current_user.id)
        .all()
    )
    
    # Get all board memberships for this user
    memberships = db.query(BoardMember).filter(BoardMember.user_id == current_user.id).all()
    
    return {
        "user_id": current_user.id,
        "user_email": current_user.email,
        "owned_boards": [
            {
                "id": board.id,
                "title": board.title,
                "owner_id": board.owner_id,
                "workspace_id": board.workspace_id
            }
            for board in owned_boards
        ],
        "member_boards": [
            {
                "id": board.id,
                "title": board.title,
                "owner_id": board.owner_id,
                "workspace_id": board.workspace_id
            }
            for board in member_boards
        ],
        "memberships": [
            {
                "board_id": membership.board_id,
                "role": membership.role.value,
                "created_at": membership.created_at.isoformat() if membership.created_at else None
            }
            for membership in memberships
        ]
    }

# -----------------------
# ایجاد برد جدید در یک ورک‌اسپیس
# -----------------------
@router.post("/", response_model=BoardSchema)
def create_board(
    board_in: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد یک برد جدید تحت ورک‌اسپیس مشخص
    """
    if not hasattr(board_in, "workspace_id") or board_in.workspace_id is None:
        raise HTTPException(status_code=400, detail="workspace_id باید مشخص شود")
    
    # Check if board with same name already exists in this workspace
    existing_board = db.query(Board).filter(
        Board.title == board_in.title,
        Board.workspace_id == board_in.workspace_id
    ).first()
    
    if existing_board:
        raise HTTPException(
            status_code=400,
            detail=f"A board with the name '{board_in.title}' already exists in this workspace. Please choose a different name."
        )
    
    new_board = Board(
        title=board_in.title,
        owner_id=current_user.id,
        workspace_id=board_in.workspace_id
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

# -----------------------
# ویرایش برد
# -----------------------
@router.put("/{board_id}", response_model=BoardSchema)
def update_board(
    board_id: int,
    board_in: BoardUpdate,  # فقط عنوان لازم است
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ویرایش عنوان یک برد (فقط مالک برد می‌تواند ویرایش کند)
    """
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    board.title = board_in.title
    db.commit()
    db.refresh(board)
    return board

# -----------------------
# حذف برد
# -----------------------
@router.delete("/{board_id}", status_code=204)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف یک برد مشخص
    """
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()
    return None

# -----------------------
# انتقال برد به ورک‌اسپیس دیگر
# -----------------------
@router.patch("/{board_id}/move", response_model=BoardSchema)
def move_board(
    board_id: int,
    new_workspace_id: int = Query(..., description="شناسه ورک‌اسپیس جدید"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    انتقال یک برد به ورک‌اسپیس دیگر (فقط مالک برد می‌تواند انتقال دهد)
    """
    # Check if user has access to the board
    if not has_board_access(db, current_user.id, board_id):
        raise HTTPException(status_code=403, detail="You don't have permission to move this board")
    
    # Get the board
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Check if user is the owner (only owner can move board)
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only board owner can move the board")
    
    # Check if a board with the same name already exists in the target workspace
    existing_board = db.query(Board).filter(
        Board.title == board.title,
        Board.workspace_id == new_workspace_id,
        Board.id != board_id  # Exclude the current board from the check
    ).first()
    
    if existing_board:
        raise HTTPException(
            status_code=400, 
            detail=f"A board with the name '{board.title}' already exists in the target workspace. Please rename the board first."
        )
    
    # Update the workspace_id
    board.workspace_id = new_workspace_id
    db.commit()
    db.refresh(board)
    
    return board

@router.post("/{board_id}/copy", response_model=BoardSchema)
def copy_board(
    board_id: int,
    new_workspace_id: int = Query(..., description="شناسه ورک‌اسپیس مقصد"),
    new_title: str = Query(None, description="عنوان جدید برای برد کپی شده (اختیاری)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    کپی کردن یک برد به ورک‌اسپیس دیگر
    """
    # Check if user has access to the board
    if not has_board_access(db, current_user.id, board_id):
        raise HTTPException(status_code=403, detail="You don't have permission to copy this board")
    
    # Get the original board
    original_board = db.query(Board).filter(Board.id == board_id).first()
    if not original_board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    # Determine the new board title
    final_title = new_title or f"{original_board.title} (Copy)"
    
    # Check if a board with the same name already exists in the target workspace
    existing_board = db.query(Board).filter(
        Board.title == final_title,
        Board.workspace_id == new_workspace_id
    ).first()
    
    if existing_board:
        raise HTTPException(
            status_code=400, 
            detail=f"A board with the name '{final_title}' already exists in the target workspace. Please choose a different name."
        )
    
    # Create new board with copied data
    new_board = Board(
        title=final_title,
        workspace_id=new_workspace_id,
        owner_id=current_user.id
    )
    
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    
    # Copy all lists and cards from the original board
    from app.models.list import List
    from app.models.card import Card
    
    # Get all lists from the original board
    original_lists = db.query(List).filter(List.board_id == board_id).all()
    
    for original_list in original_lists:
        # Create new list
        new_list = List(
            title=original_list.title,
            board_id=new_board.id,
            user_id=original_list.user_id,
            color=original_list.color
        )
        db.add(new_list)
        db.commit()
        db.refresh(new_list)
        
        # Get all cards from the original list
        original_cards = db.query(Card).filter(Card.list_id == original_list.id).all()
        
        for original_card in original_cards:
            # Create new card
            new_card = Card(
                text=original_card.text,
                description=original_card.description,
                start_date=original_card.start_date,
                end_date=original_card.end_date,
                list_id=new_list.id,
                position=original_card.position,
                members=original_card.members,
                attachments=original_card.attachments
            )
            db.add(new_card)
    
    db.commit()
    
    return new_board