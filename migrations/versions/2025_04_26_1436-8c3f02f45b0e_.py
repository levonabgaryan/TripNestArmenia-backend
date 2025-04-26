"""

Revision ID: 8c3f02f45b0e
Revises: 7ebf05e5bbac
Create Date: 2025-04-26 14:36:22.537350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8c3f02f45b0e'
down_revision: Union[str, None] = '7ebf05e5bbac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tourstatus_enum = sa.Enum('CREATED', 'IN_PROGRESS', 'ACTIVE', 'REJECTED', 'ENDED', name='tourstatus')


def upgrade():
    # Сначала создаём тип ENUM в БД
    tourstatus_enum.create(op.get_bind())

    # Теперь добавляем колонку
    op.add_column('tours', sa.Column('status', tourstatus_enum, nullable=False, server_default='CREATED'))


def downgrade():
    # При откате сначала удаляем колонку
    op.drop_column('tours', 'status')

    # Потом удаляем тип ENUM
    tourstatus_enum.drop(op.get_bind())
