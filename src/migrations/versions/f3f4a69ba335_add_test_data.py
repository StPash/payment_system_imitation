"""add_test_data

Revision ID: f3f4a69ba335
Revises: d7fe8bbb9503
Create Date: 2025-06-21 10:54:47.052172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

from src.app.utils.security import hash_password


# revision identifiers, used by Alembic.
revision: str = 'f3f4a69ba335'
down_revision: Union[str, Sequence[str], None] = 'd7fe8bbb9503'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    user_table = table(
        'user',
        column('full_name', sa.String),
        column('email', sa.String),
        column('password_hash', sa.String),
        column('is_admin', sa.Boolean)
    )

    account_table = table(
        'account',
        column('account_id', sa.Integer),
        column('balance', sa.Integer),
        column('user_id', sa.Integer)
    )

    # Вставляем тестового пользователя и получаем его ID
    op.bulk_insert(
        user_table,
        [
            {
                'full_name': 'User Test',
                'email': 'user@test.ru',
                'password_hash': hash_password('user123'),
                'is_admin': False
            }
        ]
    )

    # Вставляем тестового администратора
    op.bulk_insert(
        user_table,
        [
            {
                'full_name': 'Admin Test',
                'email': 'admin@test.ru',
                'password_hash': hash_password('admin123'),
                'is_admin': True
            }
        ]
    )

    # Получаем ID только что созданного тестового пользователя
    connection = op.get_bind()
    test_user_id = connection.execute(
        sa.text("SELECT id FROM \"user\" WHERE email = 'user@test.ru'")
    ).scalar()

    # Вставляем счет для тестового пользователя
    if test_user_id:
        op.bulk_insert(
            account_table,
            [
                {
                    'account_id': 101,  # Можно тоже динамически генерировать
                    'balance': 0,
                    'user_id': test_user_id
                }
            ]
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        sa.text("DELETE FROM \"user\" WHERE email IN ('user@test.ru', 'admin@test.ru')")
    )
    # ### end Alembic commands ###
