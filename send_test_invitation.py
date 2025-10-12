#!/usr/bin/env python3
"""
Send a test invitation to your current email
"""

import sys
import os
import requests
import json
import uuid
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def send_test_invitation():
    """Send a test invitation to your current email"""
    print("📧 SENDING TEST INVITATION")
    print("=" * 50)
    
    try:
        from app.db.database import SessionLocal
        from app.models.invitation import BoardInvitation, InvitationStatus, MemberRole
        from app.models.user import User
        from app.models.board import Board
        from app.utils.send_email import send_email
        
        db = SessionLocal()
        
        # Your current email
        your_email = "sadra.amini1006@gmail.com"
        
        # Find your user
        user = db.query(User).filter(User.email == your_email).first()
        if not user:
            print(f"❌ User not found: {your_email}")
            return False
        
        print(f"✅ Found user: {user.email}")
        
        # Find a board you own
        board = db.query(Board).filter(Board.owner_id == user.id).first()
        if not board:
            print(f"❌ No board found for user: {user.id}")
            return False
        
        print(f"✅ Found board: {board.title}")
        
        # Create a new invitation
        token = str(uuid.uuid4())
        invitation = BoardInvitation(
            board_id=board.id,
            inviter_id=user.id,
            invitee_email=your_email,
            token=token,
            role=MemberRole.MEMBER,
            status=InvitationStatus.PENDING,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        db.add(invitation)
        db.commit()
        
        print(f"✅ Invitation created with token: {token}")
        
        # Send email
        try:
            frontend_url = "http://localhost:3000"
            invite_link = f"{frontend_url}/board/{board.id}/invite/{token}"
            
            subject = f"Test Invitation to join board: {board.title}"
            body = f"""
            You have been invited to join the board "{board.title}" by {user.username}.
            
            Click the link below to accept the invitation:
            {invite_link}
            
            This invitation will expire in 7 days.
            """
            
            send_email(your_email, subject, body)
            print(f"✅ Email sent to: {your_email}")
            print(f"🔗 Invitation link: {invite_link}")
            
        except Exception as e:
            print(f"⚠️  Email sending failed: {e}")
            print(f"🔗 But you can still use this link: {invite_link}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    send_test_invitation()
