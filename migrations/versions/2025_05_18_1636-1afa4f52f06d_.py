"""

Revision ID: 1afa4f52f06d
Revises: 5b7d56fa9718
Create Date: 2025-05-18 16:36:40.227420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1afa4f52f06d'
down_revision: Union[str, None] = '5b7d56fa9718'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_accomplishers_first_name', table_name='accomplishers_')
    op.drop_index('ix_accomplishers_last_name', table_name='accomplishers_')
    op.drop_table('accomplishers_')

    op.create_table(
        'accomplishers',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('info', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_accomplishers_first_name', 'accomplishers', ['first_name'], unique=False)
    op.create_index('ix_accomplishers_last_name', 'accomplishers', ['last_name'], unique=False)

    op.add_column('tours', sa.Column('assessment', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('tours', 'assessment')

    op.create_table(
        'accomplishers_',
        sa.Column('id', sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('email', sa.VARCHAR(), nullable=False),
        sa.Column('first_name', sa.VARCHAR(), nullable=False),
        sa.Column('last_name', sa.VARCHAR(), nullable=False),
        sa.Column('phone_number', sa.VARCHAR(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('info', sa.VARCHAR(), nullable=True),
        sa.UniqueConstraint('email', name='accomplishers__email_key')
    )
    op.create_index('ix_accomplishers_first_name', 'accomplishers_', ['first_name'], unique=False)
    op.create_index('ix_accomplishers_last_name', 'accomplishers_', ['last_name'], unique=False)

    op.drop_index('ix_accomplishers_first_name', table_name='accomplishers')
    op.drop_index('ix_accomplishers_last_name', table_name='accomplishers')
    op.drop_table('accomplishers')
