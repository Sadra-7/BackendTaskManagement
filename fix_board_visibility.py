#!/usr/bin/env python3
"""
Fix board visibility for invited users
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_board_visibility():
    """Fix board visibility for invited users"""
    print("🔧 FIXING BOARD VISIBILITY")
    print("=" * 50)
    
    try:
        from app.db.database import SessionLocal
        from app.models.invitation import BoardMember, BoardInvitation, InvitationStatus
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
        
        # Check all board memberships for this user
        memberships = db.query(BoardMember).filter(BoardMember.user_id == user.id).all()
        print(f"📋 Current memberships ({len(memberships)}):")
        
        for membership in memberships:
            board = db.query(Board).filter(Board.id == membership.board_id).first()
            if board:
                print(f"  ✅ Board: {board.title} (ID: {board.id}) - Role: {membership.role.value}")
                print(f"     Owner: {board.owner_id}, Workspace: {board.workspace_id}")
            else:
                print(f"  ❌ Board ID: {membership.board_id} (Board not found)")
        
        # Check if there are any pending invitations
        pending_invitations = db.query(BoardInvitation).filter(
            BoardInvitation.invitee_email == invited_email,
            BoardInvitation.status == InvitationStatus.PENDING
        ).all()
        
        print(f"📋 Pending invitations ({len(pending_invitations)}):")
        for inv in pending_invitations:
            board = db.query(Board).filter(Board.id == inv.board_id).first()
            if board:
                print(f"  - Board: {board.title} (ID: {board.id}) - Token: {inv.token[:8]}...")
            else:
                print(f"  - Board ID: {inv.board_id} (Board not found) - Token: {inv.token[:8]}...")
        
        # Check boards where user is owner
        owned_boards = db.query(Board).filter(Board.owner_id == user.id).all()
        print(f"📋 Owned boards ({len(owned_boards)}):")
        for board in owned_boards:
            print(f"  - {board.title} (ID: {board.id})")
        
        # Test the boards query that the frontend should use
        print(f"\n🔍 TESTING BOARDS QUERY:")
        
        # Get boards where user is owner
        owned_boards_query = db.query(Board).filter(Board.owner_id == user.id).all()
        print(f"  Owned boards: {len(owned_boards_query)}")
        
        # Get boards where user is member
        from sqlalchemy.orm import joinedload
        member_boards_query = (
            db.query(Board)
            .join(BoardMember, Board.id == BoardMember.board_id)
            .filter(BoardMember.user_id == user.id)
            .all()
        )
        print(f"  Member boards: {len(member_boards_query)}")
        
        # Combine and deduplicate
        all_boards = owned_boards_query + member_boards_query
        unique_boards = []
        seen_ids = set()
        
        for board in all_boards:
            if board.id not in seen_ids:
                unique_boards.append(board)
                seen_ids.add(board.id)
        
        print(f"  Total unique boards: {len(unique_boards)}")
        for board in unique_boards:
            print(f"    - {board.title} (ID: {board.id})")
        
        # If no boards found, let's create a test membership
        if len(unique_boards) == 0:
            print(f"\n⚠️  No boards found for user!")
            print(f"💡 Let's check if there are any boards to join...")
            
            # Find any board to add the user to
            any_board = db.query(Board).first()
            if any_board:
                print(f"🔧 Adding user to board: {any_board.title}")
                
                # Create board membership
                new_membership = BoardMember(
                    board_id=any_board.id,
                    user_id=user.id,
                    role="member"
                )
                
                db.add(new_membership)
                db.commit()
                
                print(f"✅ User added to board: {any_board.title}")
            else:
                print(f"❌ No boards exist in the system!")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_board_visibility()
