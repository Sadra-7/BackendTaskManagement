#!/usr/bin/env python3
"""
Manually add user to board
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def add_user_to_board():
    """Manually add user to board"""
    print("🔧 ADDING USER TO BOARD")
    print("=" * 50)
    
    try:
        from app.db.database import SessionLocal
        from app.models.invitation import BoardMember
        from app.models.user import User
        from app.models.board import Board
        
        db = SessionLocal()
        
        # Find the user
        user_email = "s.amini8585@gmail.com"
        user = db.query(User).filter(User.email == user_email).first()
        
        if not user:
            print(f"❌ User not found: {user_email}")
            return False
        
        print(f"✅ Found user: {user.email} (ID: {user.id})")
        
        # Find any board
        board = db.query(Board).first()
        if not board:
            print(f"❌ No boards found in database")
            return False
        
        print(f"✅ Found board: {board.title} (ID: {board.id})")
        
        # Check if user is already a member
        existing_member = db.query(BoardMember).filter(
            BoardMember.board_id == board.id,
            BoardMember.user_id == user.id
        ).first()
        
        if existing_member:
            print(f"⚠️  User is already a member of this board")
            print(f"  Role: {existing_member.role.value}")
            return True
        
        # Add user to board
        new_membership = BoardMember(
            board_id=board.id,
            user_id=user.id,
            role="member"
        )
        
        db.add(new_membership)
        db.commit()
        
        print(f"✅ User added to board: {board.title}")
        print(f"  Board ID: {board.id}")
        print(f"  User ID: {user.id}")
        print(f"  Role: member")
        
        # Verify the membership
        membership = db.query(BoardMember).filter(
            BoardMember.board_id == board.id,
            BoardMember.user_id == user.id
        ).first()
        
        if membership:
            print(f"✅ Membership verified: {membership.role.value}")
        else:
            print(f"❌ Membership not found after creation")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_user_to_board()
