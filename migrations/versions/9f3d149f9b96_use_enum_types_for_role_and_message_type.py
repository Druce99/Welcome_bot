"""use enum types for role and message_type

Revision ID: 9f3d149f9b96
Revises: 2ee8c5d99db2
Create Date: 2026-06-10 12:45:59.487637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9f3d149f9b96'
down_revision: Union[str, Sequence[str], None] = '2ee8c5d99db2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


message_type_enum = postgresql.ENUM('case', 'offer', name='messagetype')
user_role_enum = postgresql.ENUM('buyer', 'owner', name='userrole')


def upgrade() -> None:
    """Upgrade schema."""
    message_type_enum.create(op.get_bind(), checkfirst=True)
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        'scheduled_messages', 'message_type',
        existing_type=sa.TEXT(),
        type_=message_type_enum,
        postgresql_using='message_type::messagetype',
        existing_nullable=False,
    )
    op.alter_column(
        'users', 'role',
        existing_type=sa.TEXT(),
        type_=user_role_enum,
        postgresql_using='role::userrole',
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users', 'role',
        existing_type=user_role_enum,
        type_=sa.TEXT(),
        existing_nullable=False,
    )
    op.alter_column(
        'scheduled_messages', 'message_type',
        existing_type=message_type_enum,
        type_=sa.TEXT(),
        existing_nullable=False,
    )

    message_type_enum.drop(op.get_bind(), checkfirst=True)
    user_role_enum.drop(op.get_bind(), checkfirst=True)
