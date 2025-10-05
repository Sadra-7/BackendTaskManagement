# app/routers/api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.workspace import Workspace
from app.models.board import Board

router = APIRouter(prefix="/api", tags=["API"])

# Pydantic models for API responses
class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str = None
    role: str = "user"
    
    class Config:
        from_attributes = True

class WorkspaceResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    board_count: int = 0
    member_count: int = 1
    is_starred: bool = False
    is_private: bool = False
    color: str = "#8b5cf6"
    created_at: str = None
    
    class Config:
        from_attributes = True

class BoardResponse(BaseModel):
    id: int
    title: str
    owner_id: int
    workspace_id: int
    background: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    is_starred: bool = False
    member_count: int = 1
    last_viewed: str = None
    created_at: str = None
    
    class Config:
        from_attributes = True

# User profile endpoint
@router.get("/user/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile information"""
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role.value if current_user.role else "user"
    )

# Workspaces endpoint
@router.get("/workspaces", response_model=List[WorkspaceResponse])
def get_user_workspaces(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all workspaces for the current user"""
    workspaces = db.query(Workspace).filter(Workspace.owner_id == current_user.id).all()
    
    # Convert to response format
    workspace_responses = []
    for workspace in workspaces:
        # Count boards in this workspace
        board_count = db.query(Board).filter(Board.workspace_id == workspace.id).count()
        
        workspace_responses.append(WorkspaceResponse(
            id=workspace.id,
            name=workspace.name,
            owner_id=workspace.owner_id,
            board_count=board_count,
            member_count=1,  # Default to 1 for now
            is_starred=False,  # Default to False for now
            is_private=False,  # Default to False for now
            color="#8b5cf6",  # Default color
            created_at=datetime.utcnow().isoformat()
        ))
    
    return workspace_responses

# Recent boards endpoint
@router.get("/boards/recent", response_model=List[BoardResponse])
def get_recent_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get recently viewed boards for the current user"""
    # Get all boards for the user, ordered by ID (most recent first)
    recent_boards = (
        db.query(Board)
        .filter(Board.owner_id == current_user.id)
        .order_by(Board.id.desc())
        .limit(10)
        .all()
    )
    
    # Convert to response format
    board_responses = []
    for board in recent_boards:
        # Handle case where workspace_id might be None
        workspace_id = board.workspace_id if board.workspace_id is not None else 1
        
        board_responses.append(BoardResponse(
            id=board.id,
            title=board.title,
            owner_id=board.owner_id,
            workspace_id=workspace_id,
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            is_starred=False,
            member_count=1,
            last_viewed="2 hours ago",  # Mock data for now
            created_at=datetime.utcnow().isoformat()
        ))
    
    return board_responses

# Create workspace endpoint
@router.post("/workspaces", response_model=WorkspaceResponse)
def create_workspace_api(
    name: str,
    description: str = None,
    color: str = "#8b5cf6",
    is_private: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new workspace"""
    workspace = Workspace(
        name=name,
        owner_id=current_user.id
    )
    
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    
    return WorkspaceResponse(
        id=workspace.id,
        name=workspace.name,
        owner_id=workspace.owner_id,
        board_count=0,
        member_count=1,
        is_starred=False,
        is_private=is_private,
        color=color,
        created_at=datetime.utcnow().isoformat()
    )

# Create board endpoint
class BoardCreateRequest(BaseModel):
    name: str
    workspace_id: int
    description: str = None
    background: str = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

@router.post("/boards", response_model=BoardResponse)
def create_board_api(
    board_data: BoardCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new board"""
    # Verify workspace ownership
    workspace = db.query(Workspace).filter(
        Workspace.id == board_data.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found or access denied")
    
    board = Board(
        title=board_data.name,  # Using title field from model
        owner_id=current_user.id,
        workspace_id=board_data.workspace_id
    )
    
    db.add(board)
    db.commit()
    db.refresh(board)
    
    return BoardResponse(
        id=board.id,
        title=board.title,
        owner_id=board.owner_id,
        workspace_id=board.workspace_id,
        background=board_data.background,
        is_starred=False,
        member_count=1,
        last_viewed="Just now",
        created_at=datetime.utcnow().isoformat()
    )

# Get boards by workspace endpoint
@router.get("/boards")
def get_boards_by_workspace(
    workspace_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get boards, optionally filtered by workspace_id"""
    query = db.query(Board).filter(Board.owner_id == current_user.id)
    
    if workspace_id:
        query = query.filter(Board.workspace_id == workspace_id)
    
    boards = query.all()
    
    return [
        BoardResponse(
            id=board.id,
            title=board.title,
            owner_id=board.owner_id,
            workspace_id=board.workspace_id,
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            is_starred=False,
            member_count=1,
            last_viewed="Just now",
            created_at=datetime.utcnow().isoformat()
        )
        for board in boards
    ]

# Toggle workspace star endpoint
@router.patch("/workspaces/{workspace_id}/star")
def toggle_workspace_star(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle star status for a workspace"""
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # For now, just return success (star functionality can be added later)
    return {"message": "Workspace star status updated", "workspace_id": workspace_id}

# Sample data creation endpoint (for development/testing)
@router.post("/sample-data")
def create_sample_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create sample workspaces and boards for testing"""
    try:
        # Create sample workspace
        workspace = Workspace(
            name="Nik Tick Workspace",
            owner_id=current_user.id
        )
        db.add(workspace)
        db.commit()
        db.refresh(workspace)
        
        # Create sample boards
        sample_boards = [
            {
                "title": "Product Roadmap",
                "workspace_id": workspace.id
            },
            {
                "title": "Sprint Planning", 
                "workspace_id": workspace.id
            },
            {
                "title": "Bug Tracking",
                "workspace_id": workspace.id
            }
        ]
        
        for board_data in sample_boards:
            board = Board(
                title=board_data["title"],
                owner_id=current_user.id,
                workspace_id=board_data["workspace_id"]
            )
            db.add(board)
        
        db.commit()
        
        return {
            "message": "Sample data created successfully",
            "workspace_id": workspace.id,
            "boards_created": len(sample_boards)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating sample data: {str(e)}")
