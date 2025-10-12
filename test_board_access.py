#!/usr/bin/env python3
"""
Test board access for invited users
"""

import sys
import os
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_board_access():
    """Test board access for invited users"""
    print("🔍 TESTING BOARD ACCESS")
    print("=" * 50)
    
    try:
        from app.db.database import SessionLocal
        from app.models.invitation import BoardMember
        from app.models.user import User
        from app.models.board import Board
        
        db = SessionLocal()
        
        # Check the invited user
        invited_email = "s.amini8585@gmail.com"
        user = db.query(User).filter(User.email == invited_email).first()
        
        if not user:
            print(f"❌ User not found: {invited_email}")
            return False
        
        print(f"✅ Found user: {user.email} (ID: {user.id})")
        
        # Check board memberships
        memberships = db.query(BoardMember).filter(BoardMember.user_id == user.id).all()
        print(f"📋 Board memberships ({len(memberships)}):")
        for membership in memberships:
            board = db.query(Board).filter(Board.id == membership.board_id).first()
            if board:
                print(f"  - Board: {board.title} (ID: {board.id}) - Role: {membership.role.value}")
            else:
                print(f"  - Board ID: {membership.board_id} (Board not found) - Role: {membership.role.value}")
        
        # Check boards where user is owner
        owned_boards = db.query(Board).filter(Board.owner_id == user.id).all()
        print(f"📋 Owned boards ({len(owned_boards)}):")
        for board in owned_boards:
            print(f"  - {board.title} (ID: {board.id})")
        
        # Check boards where user is member
        member_boards = (
            db.query(Board)
            .join(BoardMember, Board.id == BoardMember.board_id)
            .filter(BoardMember.user_id == user.id)
            .all()
        )
        print(f"📋 Member boards ({len(member_boards)}):")
        for board in member_boards:
            print(f"  - {board.title} (ID: {board.id})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test the API endpoint"""
    print(f"\n🌐 TESTING API ENDPOINT")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test debug endpoint
    try:
        response = requests.get(f"{base_url}/boards/debug/my-boards")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Debug endpoint working:")
            print(f"  User: {data['user_email']}")
            print(f"  Owned boards: {len(data['owned_boards'])}")
            print(f"  Member boards: {len(data['member_boards'])}")
            print(f"  Memberships: {len(data['memberships'])}")
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_board_access()
    test_api_endpoint()
