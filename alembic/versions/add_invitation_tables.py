"""Add invitation tables

Revision ID: add_invitation_tables
Revises: ac71f4e22c43
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_invitation_tables'
down_revision = 'ac71f4e22c43'
branch_labels = None
depends_on = None


def upgrade():
    """Add invitation tables"""
    # Create board_invitations table
    op.create_table('board_invitations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('board_id', sa.Integer(), nullable=False),
        sa.Column('inviter_id', sa.Integer(), nullable=False),
        sa.Column('invitee_email', sa.String(length=255), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, default='member'),
        sa.Column('status', sa.String(length=50), nullable=False, default='pending'),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    
    # Create board_members table
    op.create_table('board_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('board_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, default='member'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('board_id', 'user_id', name='unique_board_user')
    )
    
    # Add foreign key constraints
    op.create_foreign_key('fk_board_invitations_board_id', 'board_invitations', 'boards', ['board_id'], ['id'])
    op.create_foreign_key('fk_board_invitations_inviter_id', 'board_invitations', 'users', ['inviter_id'], ['id'])
    op.create_foreign_key('fk_board_members_board_id', 'board_members', 'boards', ['board_id'], ['id'])
    op.create_foreign_key('fk_board_members_user_id', 'board_members', 'users', ['user_id'], ['id'])


def downgrade():
    """Remove invitation tables"""
    # Drop foreign key constraints
    op.drop_constraint('fk_board_members_user_id', 'board_members', type_='foreignkey')
    op.drop_constraint('fk_board_members_board_id', 'board_members', type_='foreignkey')
    op.drop_constraint('fk_board_invitations_inviter_id', 'board_invitations', type_='foreignkey')
    op.drop_constraint('fk_board_invitations_board_id', 'board_invitations', type_='foreignkey')
    
    # Drop tables
    op.drop_table('board_members')
    op.drop_table('board_invitations')





