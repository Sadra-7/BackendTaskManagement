#!/usr/bin/env python3
"""
Comprehensive debug script for invitation system
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_invitation_system():
    """Debug the complete invitation system"""
    print("🔍 DEBUGGING INVITATION SYSTEM")
    print("=" * 60)
    
    try:
        # Import database models
        from app.db.database import SessionLocal
        from app.models.invitation import BoardInvitation, BoardMember, InvitationStatus
        from app.models.user import User
        from app.models.board import Board
        
        db = SessionLocal()
        
        print("✅ Database connection successful")
        
        # Check all users
        print("\n📋 ALL USERS:")
        users = db.query(User).all()
        for user in users:
            print(f"  - ID: {user.id}, Email: {user.email}, Username: {user.username}")
        
        # Check all boards
        print("\n📋 ALL BOARDS:")
        boards = db.query(Board).all()
        for board in boards:
            print(f"  - ID: {board.id}, Title: {board.title}, Owner: {board.owner_id}")
        
        # Check all invitations
        print("\n📋 ALL INVITATIONS:")
        invitations = db.query(BoardInvitation).all()
        for inv in invitations:
            print(f"  - ID: {inv.id}, Token: {inv.token[:8]}..., Invitee: {inv.invitee_email}, Status: {inv.status}")
            print(f"    Board: {inv.board_id}, Inviter: {inv.inviter_id}, Expires: {inv.expires_at}")
        
        # Check all board members
        print("\n📋 ALL BOARD MEMBERS:")
        members = db.query(BoardMember).all()
        for member in members:
            print(f"  - Board: {member.board_id}, User: {member.user_id}, Role: {member.role}")
        
        # Test specific invitation
        test_token = "3c51d64b-fbb2-4f16-ba6b-e451e10b52ff"
        print(f"\n🔍 TESTING INVITATION TOKEN: {test_token}")
        
        invitation = db.query(BoardInvitation).filter(
            BoardInvitation.token == test_token
        ).first()
        
        if invitation:
            print(f"✅ Invitation found:")
            print(f"  - ID: {invitation.id}")
            print(f"  - Invitee: {invitation.invitee_email}")
            print(f"  - Status: {invitation.status}")
            print(f"  - Board ID: {invitation.board_id}")
            print(f"  - Inviter ID: {invitation.inviter_id}")
            print(f"  - Expires: {invitation.expires_at}")
            
            # Check if expired
            if invitation.expires_at and datetime.utcnow() > invitation.expires_at:
                print("⚠️  INVITATION IS EXPIRED!")
            else:
                print("✅ Invitation is not expired")
            
            # Check board details
            board = db.query(Board).filter(Board.id == invitation.board_id).first()
            if board:
                print(f"✅ Board found: {board.title} (Owner: {board.owner_id})")
            else:
                print("❌ Board not found!")
            
            # Check inviter details
            inviter = db.query(User).filter(User.id == invitation.inviter_id).first()
            if inviter:
                print(f"✅ Inviter found: {inviter.email} ({inviter.username})")
            else:
                print("❌ Inviter not found!")
                
        else:
            print("❌ Invitation not found!")
        
        # Test email matching logic
        print(f"\n🔍 EMAIL MATCHING TEST:")
        user_email = "sadra.amini1006@gmail.com"
        invitee_email = "s.amini8585@gmail.com"
        
        user_email_lower = user_email.lower().strip()
        invitee_email_lower = invitee_email.lower().strip()
        
        print(f"  User email: '{user_email}' -> '{user_email_lower}'")
        print(f"  Invitee email: '{invitee_email}' -> '{invitee_email_lower}'")
        print(f"  Match: {user_email_lower == invitee_email_lower}")
        
        # Check if user exists
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            print(f"✅ User found: {user.email} (ID: {user.id})")
        else:
            print("❌ User not found!")
        
        # Check if invitee exists
        invitee = db.query(User).filter(User.email == invitee_email).first()
        if invitee:
            print(f"✅ Invitee found: {invitee.email} (ID: {invitee.id})")
        else:
            print("❌ Invitee not found!")
        
        print(f"\n🎯 RECOMMENDATIONS:")
        print(f"1. Login as the invited user: {invitee_email}")
        print(f"2. Or send a new invitation to: {user_email}")
        print(f"3. Check if the invitation is expired")
        print(f"4. Verify the invitation token is correct")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print(f"\n🌐 TESTING API ENDPOINTS")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test server
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server running: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False
    
    # Test docs
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"✅ API docs available")
    except Exception as e:
        print(f"❌ API docs not accessible: {e}")
    
    return True

if __name__ == "__main__":
    print("Starting comprehensive invitation system debug...")
    
    # Test API endpoints
    test_api_endpoints()
    
    # Debug database
    debug_invitation_system()
    
    print(f"\n🎉 Debug completed!")
    print(f"Check the output above for any issues.")