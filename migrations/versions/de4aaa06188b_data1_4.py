"""data1.4

Revision ID: de4aaa06188b
Revises: 147807238f59
Create Date: 2024-08-06 23:11:45.142634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de4aaa06188b'
down_revision = '147807238f59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'content',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'content',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###