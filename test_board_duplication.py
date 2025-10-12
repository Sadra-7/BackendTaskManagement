#!/usr/bin/env python3
"""
Test board duplication functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.board import Board
from app.models.list import List
from app.models.card import Card
from app.models.user import User
from app.utils.board_duplicator import duplicate_board_for_user, get_board_data

def test_board_duplication():
    """Test board duplication functionality"""
    db = SessionLocal()
    
    try:
        print("🧪 TESTING BOARD DUPLICATION")
        print("=" * 50)
        
        # Get users
        users = db.query(User).all()
        if len(users) < 2:
            print("❌ Need at least 2 users to test duplication")
            return False
        
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  - User {user.id}: {user.username}")
        
        # Get boards
        boards = db.query(Board).all()
        if len(boards) < 1:
            print("❌ Need at least 1 board to test duplication")
            return False
        
        print(f"\nFound {len(boards)} boards:")
        for board in boards:
            print(f"  - Board {board.id}: {board.title} (Owner: {board.owner_id})")
        
        # Test duplication
        original_board_id = boards[0].id
        new_user_id = users[1].id
        
        print(f"\n🔄 Duplicating Board {original_board_id} for User {new_user_id}...")
        
        # Get original board data
        original_data = get_board_data(db, original_board_id)
        print(f"Original board has {len(original_data['lists'])} lists")
        
        # Duplicate the board
        new_board_id = duplicate_board_for_user(db, original_board_id, new_user_id)
        print(f"✅ Board duplicated! New board ID: {new_board_id}")
        
        # Get new board data
        new_data = get_board_data(db, new_board_id)
        print(f"New board has {len(new_data['lists'])} lists")
        
        # Compare the data
        print("\n📊 COMPARISON:")
        print(f"Original board: {original_data['board']['title']}")
        print(f"New board: {new_data['board']['title']}")
        print(f"Original lists: {len(original_data['lists'])}")
        print(f"New lists: {len(new_data['lists'])}")
        
        # Check if lists and cards were copied
        if len(original_data['lists']) == len(new_data['lists']):
            print("✅ Lists copied successfully")
        else:
            print("❌ Lists not copied correctly")
        
        # Check cards
        original_cards = sum(len(list_data['cards']) for list_data in original_data['lists'])
        new_cards = sum(len(list_data['cards']) for list_data in new_data['lists'])
        
        print(f"Original cards: {original_cards}")
        print(f"New cards: {new_cards}")
        
        if original_cards == new_cards:
            print("✅ Cards copied successfully")
        else:
            print("❌ Cards not copied correctly")
        
        print("\n🎉 Board duplication test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_board_duplication()
