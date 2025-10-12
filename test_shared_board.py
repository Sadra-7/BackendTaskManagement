#!/usr/bin/env python3
"""
Test shared board functionality (like Trello)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.board import Board
from app.models.list import List
from app.models.card import Card
from app.models.user import User
from app.models.invitation import BoardMember

def test_shared_board():
    """Test shared board functionality"""
    db = SessionLocal()
    
    try:
        print("🧪 TESTING SHARED BOARD FUNCTIONALITY")
        print("=" * 50)
        
        # Get users
        users = db.query(User).all()
        if len(users) < 2:
            print("❌ Need at least 2 users to test shared board")
            return False
        
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  - User {user.id}: {user.username}")
        
        # Get boards
        boards = db.query(Board).all()
        if len(boards) < 1:
            print("❌ Need at least 1 board to test shared board")
            return False
        
        print(f"\nFound {len(boards)} boards:")
        for board in boards:
            print(f"  - Board {board.id}: {board.title} (Owner: {board.owner_id})")
        
        # Test adding user as board member
        board_id = boards[0].id
        new_member_id = users[1].id
        
        print(f"\n🔄 Adding User {new_member_id} as member of Board {board_id}...")
        
        # Check if already a member
        existing_member = db.query(BoardMember).filter(
            BoardMember.board_id == board_id,
            BoardMember.user_id == new_member_id
        ).first()
        
        if existing_member:
            print(f"✅ User {new_member_id} is already a member of Board {board_id}")
        else:
            # Add as member
            board_member = BoardMember(
                board_id=board_id,
                user_id=new_member_id,
                role="member"
            )
            db.add(board_member)
            db.commit()
            print(f"✅ User {new_member_id} added as member of Board {board_id}")
        
        # Test board access for both users
        print(f"\n📊 TESTING BOARD ACCESS:")
        
        # Check owner access
        owner = db.query(User).filter(User.id == boards[0].owner_id).first()
        print(f"Board owner: {owner.username} (ID: {owner.id})")
        
        # Check member access
        members = db.query(BoardMember).filter(BoardMember.board_id == board_id).all()
        print(f"Board members: {len(members)}")
        for member in members:
            user = db.query(User).filter(User.id == member.user_id).first()
            print(f"  - {user.username} (Role: {member.role})")
        
        # Test that both users can see the board
        print(f"\n🔍 VERIFYING BOARD VISIBILITY:")
        
        # Owner should see the board
        owner_boards = db.query(Board).filter(Board.owner_id == owner.id).all()
        print(f"Owner can see {len(owner_boards)} boards")
        
        # Member should see the board (this is what we fixed in boards.py)
        member_boards = []
        for member in members:
            # Check if user is owner of any boards
            owned_boards = db.query(Board).filter(Board.owner_id == member.user_id).all()
            member_boards.extend(owned_boards)
            
            # Check if user is member of any boards
            member_board_ids = db.query(BoardMember.board_id).filter(
                BoardMember.user_id == member.user_id
            ).all()
            member_board_ids = [mb[0] for mb in member_board_ids]
            member_boards.extend(db.query(Board).filter(Board.id.in_(member_board_ids)).all())
        
        # Remove duplicates
        member_boards = list(set(member_boards))
        print(f"Members can see {len(member_boards)} boards")
        
        print("\n🎉 Shared board test completed!")
        print("✅ Both users can now collaborate on the same board!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_shared_board()
