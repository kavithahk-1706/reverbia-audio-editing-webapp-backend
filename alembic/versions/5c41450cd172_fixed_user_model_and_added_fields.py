"""fixed user model and added fields

Revision ID: 5c41450cd172
Revises: 01ad51a49bf9
Create Date: 2025-05-24 13:45:48.229823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c41450cd172'
down_revision: Union[str, None] = '01ad51a49bf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('dob', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('country', sa.String(), nullable=True))
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'country')
    op.drop_column('users', 'dob')
    # ### end Alembic commands ###
