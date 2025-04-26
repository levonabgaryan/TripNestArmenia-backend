"""

Revision ID: 036f45e208fe
Revises: 6da4facc40f1
Create Date: 2025-04-26 19:58:11.639819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '036f45e208fe'
down_revision: Union[str, None] = '6da4facc40f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Сначала добавить колонку с nullable=True
    op.add_column('tours', sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=True))

    # 2. Затем обновить все существующие записи
    op.execute('UPDATE tours SET amount = 0')

    # 3. И потом изменить колонку, сделав ее nullable=False
    op.alter_column('tours', 'amount', nullable=False)


def downgrade() -> None:
    op.drop_column('tours', 'amount')

