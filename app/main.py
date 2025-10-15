import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.db.database import engine, Base, SessionLocal, get_db
from sqlalchemy.orm import Session
from app.routers.users import router as users_router
from app.routers import users, boards, cards, list_router, admin, workspaces, api, card_members, invitations
from app.routers.boards import router as boards_router
from app.routers.list_router import router as list_router
from app.routers import cards  # اضافه شد
from app.models.user import User, UserRole
from app.utils.hashing import hash_password
from app.auth.dependencies import get_current_user


# Load environment variables
load_dotenv()

# Create tables (در صورت استفاده از Alembic فقط برای dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager Backend")

# CORS middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://niktick.ir",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)            
app.include_router(boards_router)           
app.include_router(list_router)             
app.include_router(cards.router)            
app.include_router(admin.router)        
app.include_router(workspaces.router)
app.include_router(api.router)
app.include_router(card_members.router)
# app.include_router(invitations.router)  # Commented out to avoid conflicts   


# Root endpoint
@app.get("/")
def root():
    return {"message": "Task Manager Backend is Running ✅"}

# Test endpoint for invitations
@app.get("/test-invitations")
def test_invitations():
    return {"message": "Invitations router is working", "status": "OK"}

# Send invitation endpoint
@app.post("/invitations/send")
async def send_invitation(
    invitation_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send board invitation"""
    try:
        from app.models.invitation import BoardInvitation, InvitationStatus, MemberRole
        from app.models.board import Board
        from datetime import datetime, timedelta
        import uuid
        
        board_id = invitation_data.get("board_id")
        invitee_email = invitation_data.get("invitee_email")
        role = invitation_data.get("role", "member")
        
        if not board_id or not invitee_email:
            raise HTTPException(status_code=400, detail="board_id and invitee_email are required")
        
        # Check if board exists and user is owner
        board = db.query(Board).filter(Board.id == board_id).first()
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        
        if board.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only board owner can send invitations")
        
        # Check if user is already a member
        from app.models.invitation import BoardMember
        existing_member = db.query(BoardMember).filter(
            BoardMember.board_id == board_id,
            BoardMember.user_id == current_user.id
        ).first()
        
        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member of this board")
        
        # Generate token
        token = str(uuid.uuid4())
        
        # Create invitation
        invitation = BoardInvitation(
            board_id=board_id,
            inviter_id=current_user.id,
            invitee_email=invitee_email,
            token=token,
            role=MemberRole(role),
            status=InvitationStatus.PENDING,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        
        # Send email
        try:
            from app.utils.send_email import send_email
            import os
            
            frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
            invite_link = f"{frontend_url}/board/{board_id}/invite/{token}"
            
            subject = f"Invitation to join board: {board.title}"
            body = f"""
            You have been invited to join the board "{board.title}" by {current_user.username}.
            
            Click the link below to accept the invitation:
            {invite_link}
            
            This invitation will expire in 7 days.
            """
            
            print(f"DEBUG: Sending email to {invitee_email}")
            print(f"DEBUG: Email subject: {subject}")
            print(f"DEBUG: Invite link: {invite_link}")
            
            send_email(invitee_email, subject, body)
            print(f"DEBUG: Email sent successfully to {invitee_email}")
            
        except Exception as email_error:
            print(f"ERROR: Failed to send email: {email_error}")
            # Don't fail the entire request if email fails
            # The invitation is still created in the database
        
        return {
            "message": "Invitation sent successfully",
            "invitation_id": invitation.id,
            "token": token
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get invitation by token endpoint
@app.get("/invitations/token/{token}")
async def get_invitation_by_token(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get invitation details by token"""
    try:
        from app.models.invitation import BoardInvitation
        
        invitation = db.query(BoardInvitation).filter(
            BoardInvitation.token == token
        ).first()

        if not invitation:
            raise HTTPException(
                status_code=404,
                detail="Invalid invitation token"
            )

        # Get board details
        from app.models.board import Board
        board = db.query(Board).filter(Board.id == invitation.board_id).first()
        if not board:
            raise HTTPException(
                status_code=404,
                detail="Board not found"
            )

        # Get inviter details
        from app.models.user import User
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Direct accept endpoint (backup)
@app.post("/invitations/accept")
async def accept_invitation_direct(
    invitation_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Direct accept invitation endpoint"""
    try:
        # Import models
        from app.models.invitation import BoardInvitation, BoardMember, InvitationStatus, MemberRole
        from datetime import datetime
        
        token = invitation_data.get("token")
        if not token:
            raise HTTPException(status_code=400, detail="Token is required")
        
        print(f"DEBUG: Looking for invitation with token: {token}")
        
        # Find invitation by token
        invitation = db.query(BoardInvitation).filter(
            BoardInvitation.token == token
        ).first()

        if not invitation:
            print("ERROR: Invitation not found")
            raise HTTPException(
                status_code=404,
                detail="Invalid invitation token"
            )
        
        print(f"DEBUG: Found invitation - ID: {invitation.id}, Invitee: {invitation.invitee_email}, Status: {invitation.status}")

        # Check if invitation is expired (simplified check)
        if invitation.expires_at and datetime.utcnow() > invitation.expires_at:
            invitation.status = InvitationStatus.EXPIRED
            db.commit()
            raise HTTPException(
                status_code=400,
                detail="Invitation has expired"
            )

        # Check if invitation is already accepted or declined
        if invitation.status != InvitationStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail="Invitation has already been processed"
            )

        # Check if user email matches invitation email (case-insensitive)
        user_email_lower = current_user.email.lower().strip()
        invitee_email_lower = invitation.invitee_email.lower().strip()
        
        print(f"DEBUG: User email: {current_user.email} -> {user_email_lower}")
        print(f"DEBUG: Invitation email: {invitation.invitee_email} -> {invitee_email_lower}")
        print(f"DEBUG: Email match: {user_email_lower == invitee_email_lower}")
        
        if user_email_lower != invitee_email_lower:
            print(f"ERROR: Email mismatch - User: {user_email_lower}, Invitee: {invitee_email_lower}")
            raise HTTPException(
                status_code=403,
                detail=f"This invitation is for {invitation.invitee_email}, but you are logged in as {current_user.email}. Please login with the correct email address or ask the board owner to send a new invitation to your current email."
            )

        # Check if user is already a member
        existing_member = db.query(BoardMember).filter(
            BoardMember.board_id == invitation.board_id,
            BoardMember.user_id == current_user.id
        ).first()

        if existing_member:
            raise HTTPException(
                status_code=400,
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
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Get board invitations endpoint
@app.get("/invitations/board/{board_id}")
async def get_board_invitations(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all invitations for a specific board"""
    try:
        from app.models.invitation import BoardInvitation
        from app.models.board import Board
        
        # Check if user has access to the board
        board = db.query(Board).filter(Board.id == board_id).first()
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        
        # Check if user is board owner
        if board.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only board owner can view invitations")
        
        # Get all invitations for the board
        invitations = db.query(BoardInvitation).filter(
            BoardInvitation.board_id == board_id
        ).all()
        
        return {
            "board_id": board_id,
            "invitations": [
                {
                    "id": inv.id,
                    "invitee_email": inv.invitee_email,
                    "role": inv.role.value,
                    "status": inv.status.value,
                    "created_at": inv.created_at.isoformat() if inv.created_at else None,
                    "expires_at": inv.expires_at.isoformat() if inv.expires_at else None
                }
                for inv in invitations
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Check if user can accept invitation
@app.get("/invitations/check/{token}")
async def check_invitation_access(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if current user can accept the invitation"""
    try:
        from app.models.invitation import BoardInvitation
        
        # Find invitation by token
        invitation = db.query(BoardInvitation).filter(
            BoardInvitation.token == token
        ).first()

        if not invitation:
            return {
                "can_accept": False,
                "reason": "Invalid invitation token",
                "user_email": current_user.email,
                "invitation_email": None
            }

        # Check email match (case-insensitive)
        user_email_lower = current_user.email.lower().strip()
        invitee_email_lower = invitation.invitee_email.lower().strip()
        
        can_accept = user_email_lower == invitee_email_lower
        
        return {
            "can_accept": can_accept,
            "reason": "Email mismatch" if not can_accept else "Can accept",
            "user_email": current_user.email,
            "invitation_email": invitation.invitee_email,
            "board_id": invitation.board_id,
            "status": invitation.status.value
        }
        
    except Exception as e:
        return {
            "can_accept": False,
            "reason": f"Error: {str(e)}",
            "user_email": current_user.email,
            "invitation_email": None
        }

# Debug token endpoint
@app.get("/debug-token")
def debug_token(current_user: User = Depends(get_current_user)):
    return {"user": current_user}

# Initialize superadmin on startup
def init_superadmin(db):
    superadmin_email = "sadra.amini1006@gmail.com"
    existing = db.query(User).filter(User.email == superadmin_email).first()

    if not existing:
        new_superadmin = User(
            username="superadmin",
            email=superadmin_email,
            hashed_password=hash_password("admin1234"),
            role=UserRole.SUPERADMIN
        )
        db.add(new_superadmin)
        db.commit()
        print(f"SUCCESS: Superadmin created -> Email: {superadmin_email} | Password: admin1234")
    else:
        print("INFO: Superadmin already exists.")

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        init_superadmin(db)
    finally:
        db.close()