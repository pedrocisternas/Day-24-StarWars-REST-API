"""empty message

Revision ID: 36d81b456197
Revises: c7cd47574eb3
Create Date: 2021-07-15 00:30:53.223617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '36d81b456197'
down_revision = 'c7cd47574eb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorite', sa.Column('username', sa.String(length=120), nullable=True))
    op.drop_constraint('favorite_ibfk_1', 'favorite', type_='foreignkey')
    op.create_foreign_key(None, 'favorite', 'user', ['username'], ['username'])
    op.drop_column('favorite', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorite', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'favorite', type_='foreignkey')
    op.create_foreign_key('favorite_ibfk_1', 'favorite', 'user', ['user_id'], ['id'])
    op.drop_column('favorite', 'username')
    # ### end Alembic commands ###