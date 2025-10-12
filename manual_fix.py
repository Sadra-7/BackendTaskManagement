#!/usr/bin/env python3
"""
Manual fix for board membership
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.invitation import BoardMember, MemberRole
from app.models.board import Board
from app.models.user import User

def manual_fix():
    """Manually add a board member for testing"""
    db = SessionLocal()
    
    try:
        print("🔧 MANUAL BOARD MEMBERSHIP FIX")
        print("=" * 40)
        
        # Get all users
        users = db.query(User).all()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  - User {user.id}: {user.username} ({user.email})")
        
        # Get all boards
        boards = db.query(Board).all()
        print(f"\nFound {len(boards)} boards:")
        for board in boards:
            print(f"  - Board {board.id}: {board.title} (Owner: {board.owner_id})")
        
        if len(users) >= 2 and len(boards) >= 1:
            # Add the second user as a member of the first board
            user_id = users[1].id
            board_id = boards[0].id
            
            # Check if membership already exists
            existing = db.query(BoardMember).filter(
                BoardMember.user_id == user_id,
                BoardMember.board_id == board_id
            ).first()
            
            if not existing:
                # Create board membership
                member = BoardMember(
                    board_id=board_id,
                    user_id=user_id,
                    role=MemberRole.MEMBER
                )
                db.add(member)
                db.commit()
                print(f"\n✅ Added User {user_id} as member of Board {board_id}")
            else:
                print(f"\n✅ User {user_id} is already a member of Board {board_id}")
        
        # Show current memberships
        members = db.query(BoardMember).all()
        print(f"\nCurrent board memberships: {len(members)}")
        for member in members:
            print(f"  - Board {member.board_id}: User {member.user_id} (Role: {member.role})")
        
    except Exception as e:
        print(f"❌ Manual fix failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    manual_fix()
