#!/usr/bin/env python3
"""
Fix invitation system issues
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_invitation_issue():
    """Fix the invitation system issue"""
    print("🔧 FIXING INVITATION SYSTEM")
    print("=" * 50)
    
    try:
        from app.db.database import SessionLocal
        from app.models.invitation import BoardInvitation, BoardMember, InvitationStatus
        from app.models.user import User
        from app.models.board import Board
        
        db = SessionLocal()
        
        # Find the problematic invitation
        test_token = "3c51d64b-fbb2-4f16-ba6b-e451e10b52ff"
        invitation = db.query(BoardInvitation).filter(
            BoardInvitation.token == test_token
        ).first()
        
        if not invitation:
            print("❌ Invitation not found!")
            return False
        
        print(f"✅ Found invitation: {invitation.id}")
        print(f"  Invitee: {invitation.invitee_email}")
        print(f"  Status: {invitation.status}")
        
        # Check if invitation is expired
        if invitation.expires_at and datetime.utcnow() > invitation.expires_at:
            print("⚠️  Invitation is expired, extending it...")
            invitation.expires_at = datetime.utcnow() + timedelta(days=7)
            db.commit()
            print("✅ Invitation expiry extended")
        
        # Check if user exists for the invitee email
        invitee_user = db.query(User).filter(User.email == invitation.invitee_email).first()
        if not invitee_user:
            print(f"❌ User not found for email: {invitation.invitee_email}")
            print("💡 You need to register this email first!")
            return False
        
        print(f"✅ Invitee user found: {invitee_user.email}")
        
        # Check if user is already a member
        existing_member = db.query(BoardMember).filter(
            BoardMember.board_id == invitation.board_id,
            BoardMember.user_id == invitee_user.id
        ).first()
        
        if existing_member:
            print("⚠️  User is already a member of this board!")
            print("💡 The invitation might have been accepted already")
            return True
        
        print(f"✅ User is not a member yet")
        print(f"🎯 To fix this issue:")
        print(f"1. Login as: {invitation.invitee_email}")
        print(f"2. Accept the invitation")
        print(f"3. Or send a new invitation to your current email")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_invitation_issue()
