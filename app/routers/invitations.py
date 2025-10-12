from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import uuid
import os
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.invitation import BoardInvitation, BoardMember, InvitationStatus, MemberRole
from app.models.user import User
from app.models.board import Board
from app.auth.dependencies import get_current_user
from app.utils.send_email import send_email

router = APIRouter(prefix="/invitations", tags=["invitations"])

# Pydantic models
class InvitationCreate(BaseModel):
    board_id: int
    invitee_email: EmailStr
    role: str = "member"

class InvitationResponse(BaseModel):
    id: int
    token: str
    board_id: int
    inviter_id: int
    invitee_email: str
    role: str
    status: str
    expires_at: str
    created_at: str
    accepted_at: Optional[str] = None

class InvitationAccept(BaseModel):
    token: str

class BoardMemberResponse(BaseModel):
    id: int
    board_id: int
    user_id: int
    role: str
    joined_at: str
    user: dict

@router.post("/send", response_model=InvitationResponse)
async def send_invitation(
    invitation_data: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send board invitation to user
    """
    # Check if board exists and user has permission
    board = db.query(Board).filter(Board.id == invitation_data.board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    # Check if user is board owner or admin
    if board.owner_id != current_user.id:
        # Check if user is board member with admin role
        member = db.query(BoardMember).filter(
            BoardMember.board_id == invitation_data.board_id,
            BoardMember.user_id == current_user.id,
            BoardMember.role == MemberRole.ADMIN
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to invite members to this board"
            )
    
    # Check if user is already a member
    existing_member = db.query(BoardMember).filter(
        BoardMember.board_id == invitation_data.board_id,
        BoardMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this board"
        )
    
    # Check if invitation already exists and is pending
    existing_invitation = db.query(BoardInvitation).filter(
        BoardInvitation.board_id == invitation_data.board_id,
        BoardInvitation.invitee_email == invitation_data.invitee_email,
        BoardInvitation.status == InvitationStatus.PENDING
    ).first()
    
    if existing_invitation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation already sent to this email"
        )
    
    # Create invitation
    invitation = BoardInvitation(
        board_id=invitation_data.board_id,
        inviter_id=current_user.id,
        invitee_email=invitation_data.invitee_email,
        role=MemberRole(invitation_data.role),
        status=InvitationStatus.PENDING,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    # Send invitation email
    invitation_link = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/board/{invitation_data.board_id}/invite/{invitation.token}"
    
    # Create email content
    subject = f"You're invited to collaborate on '{board.title}'"
    email_body = f"""
    Hello!
    
    {current_user.username} has invited you to collaborate on the board "{board.title}".
    
    Role: {invitation_data.role.title()}
    
    To accept this invitation, click the link below:
    {invitation_link}
    
    This invitation will expire in 7 days.
    If you don't have an account, you'll be prompted to create one.
    
    If you didn't expect this invitation, you can safely ignore this email.
    
    Best regards,
    Task Manager Team
    """
    
    try:
        send_email(
            to_email=invitation_data.invitee_email,
            subject=subject,
            body=email_body
        )
    except Exception as e:
        print(f"Failed to send invitation email: {e}")
        # Continue anyway - invitation is still created
    
    return InvitationResponse(**invitation.to_dict())

@router.get("/board/{board_id}", response_model=List[InvitationResponse])
async def get_board_invitations(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all invitations for a board
    """
    # Check if user has permission to view invitations
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    if board.owner_id != current_user.id:
        # Check if user is board member with admin role
        member = db.query(BoardMember).filter(
            BoardMember.board_id == board_id,
            BoardMember.user_id == current_user.id,
            BoardMember.role == MemberRole.ADMIN
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view invitations for this board"
            )
    
    invitations = db.query(BoardInvitation).filter(
        BoardInvitation.board_id == board_id
    ).all()
    
    return [InvitationResponse(**invitation.to_dict()) for invitation in invitations]

@router.get("/token/{token}")
async def get_invitation_by_token(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get invitation details by token
    """
    invitation = db.query(BoardInvitation).filter(
        BoardInvitation.token == token
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation token"
        )
    
    # Get board details
    board = db.query(Board).filter(Board.id == invitation.board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    # Get inviter details
    inviter = db.query(User).filter(User.id == invitation.inviter_id).first()
    
    return {
        "board_id": board.id,
        "board_title": board.title,
        "inviter_name": inviter.username if inviter else "Unknown",
        "inviter_email": inviter.email if inviter else "unknown@example.com",
        "role": invitation.role.value,
        "expires_at": invitation.expires_at.isoformat() if invitation.expires_at else None,
        "status": invitation.status.value
    }

@router.post("/accept")
async def accept_invitation(
    invitation_data: InvitationAccept,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Accept board invitation
    """
    # Find invitation by token
    invitation = db.query(BoardInvitation).filter(
        BoardInvitation.token == invitation_data.token
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation token"
        )
    
    # Check if invitation is expired
    if invitation.is_expired():
        invitation.status = InvitationStatus.EXPIRED
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has expired"
        )
    
    # Check if invitation is already accepted or declined
    if invitation.status != InvitationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has already been processed"
        )
    
    # Check if user email matches invitation email
    if current_user.email != invitation.invitee_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation is not for your email address"
        )
    
    # Check if user is already a member
    existing_member = db.query(BoardMember).filter(
        BoardMember.board_id == invitation.board_id,
        BoardMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of this board"
        )
    
    # Add user as member of the same board (like Trello)
    board_member = BoardMember(
        board_id=invitation.board_id,
        user_id=current_user.id,
        role=invitation.role
    )
    
    db.add(board_member)
    
    # Update invitation status
    invitation.status = InvitationStatus.ACCEPTED
    invitation.accepted_at = datetime.utcnow()
    
    db.commit()
    db.refresh(board_member)
    
    return {
        "message": "Successfully joined the board!",
        "board_id": invitation.board_id,
        "user_id": current_user.id,
        "role": invitation.role.value
    }

@router.post("/decline")
async def decline_invitation(
    invitation_data: InvitationAccept,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Decline board invitation
    """
    # Find invitation by token
    invitation = db.query(BoardInvitation).filter(
        BoardInvitation.token == invitation_data.token
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation token"
        )
    
    # Check if invitation is already processed
    if invitation.status != InvitationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has already been processed"
        )
    
    # Check if user email matches invitation email
    if current_user.email != invitation.invitee_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This invitation is not for your email address"
        )
    
    # Update invitation status
    invitation.status = InvitationStatus.DECLINED
    
    db.commit()
    
    return {"message": "Invitation declined successfully"}

@router.delete("/{invitation_id}")
async def cancel_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel/delete invitation
    """
    invitation = db.query(BoardInvitation).filter(
        BoardInvitation.id == invitation_id
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found"
        )
    
    # Check if user has permission to cancel invitation
    if invitation.inviter_id != current_user.id:
        # Check if user is board owner or admin
        board = db.query(Board).filter(Board.id == invitation.board_id).first()
        if board.owner_id != current_user.id:
            member = db.query(BoardMember).filter(
                BoardMember.board_id == invitation.board_id,
                BoardMember.user_id == current_user.id,
                BoardMember.role == MemberRole.ADMIN
            ).first()
            if not member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to cancel this invitation"
                )
    
    db.delete(invitation)
    db.commit()
    
    return {"message": "Invitation cancelled successfully"}

@router.get("/board/{board_id}/members", response_model=List[BoardMemberResponse])
async def get_board_members(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all members of a board
    """
    # Check if user is a member of the board
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    # Check if user is board owner or member
    if board.owner_id != current_user.id:
        member = db.query(BoardMember).filter(
            BoardMember.board_id == board_id,
            BoardMember.user_id == current_user.id
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view members of this board"
            )
    
    members = db.query(BoardMember).filter(
        BoardMember.board_id == board_id
    ).all()
    
    return [BoardMemberResponse(**member.to_dict()) for member in members]

@router.delete("/board/{board_id}/members/{user_id}")
async def remove_board_member(
    board_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove member from board
    """
    # Check if user has permission to remove members
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    if board.owner_id != current_user.id:
        # Check if user is board admin
        member = db.query(BoardMember).filter(
            BoardMember.board_id == board_id,
            BoardMember.user_id == current_user.id,
            BoardMember.role == MemberRole.ADMIN
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to remove members from this board"
            )
    
    # Find member to remove
    member_to_remove = db.query(BoardMember).filter(
        BoardMember.board_id == board_id,
        BoardMember.user_id == user_id
    ).first()
    
    if not member_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Don't allow removing board owner
    if board.owner_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove board owner"
        )
    
    db.delete(member_to_remove)
    db.commit()
    
    return {"message": "Member removed successfully"}

@router.put("/board/{board_id}/members/{user_id}/role")
async def update_member_role(
    board_id: int,
    user_id: int,
    new_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update member role
    """
    # Check if user has permission to update member roles
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    if board.owner_id != current_user.id:
        # Check if user is board admin
        member = db.query(BoardMember).filter(
            BoardMember.board_id == board_id,
            BoardMember.user_id == current_user.id,
            BoardMember.role == MemberRole.ADMIN
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update member roles"
            )
    
    # Find member to update
    member_to_update = db.query(BoardMember).filter(
        BoardMember.board_id == board_id,
        BoardMember.user_id == user_id
    ).first()
    
    if not member_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Update role
    member_to_update.role = MemberRole(new_role)
    db.commit()
    
    return {"message": "Member role updated successfully"}
