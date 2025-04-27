from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0755f806803a'
down_revision: Union[str, None] = 'bd4c307a8438'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Обновляем все строки с NULL в amount_by_dram на 0
    op.execute("UPDATE tours SET amount_by_dram = 0 WHERE amount_by_dram IS NULL")

    # Далее создаём таблицу, индекс и выполняем другие операции
    op.create_table(
        'admin_chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['admin_id'], ['admins.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_admin_chat_messages_id'), 'admin_chat_messages', ['id'], unique=False)

    op.alter_column(
        'tours',
        'amount_by_dram',
        existing_type=sa.NUMERIC(precision=12, scale=2),
        nullable=False
    )
