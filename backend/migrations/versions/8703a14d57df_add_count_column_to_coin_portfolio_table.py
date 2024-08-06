"""Add count column to coin_portfolio table

Revision ID: 8703a14d57df
Revises: 
Create Date: 2024-08-03 22:20:52.847698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8703a14d57df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coin',
    sa.Column('coinid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('symbol', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('change24hrpercentage', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('coinid')
    )
    op.create_table('portfolio',
    sa.Column('portfolioid', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('portfolioid')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('username')
    )
    op.create_table('coin_portfolio',
    sa.Column('coin_coinid', sa.Integer(), nullable=False),
    sa.Column('portfolio_portfolioid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coin_coinid'], ['coin.coinid'], ),
    sa.ForeignKeyConstraint(['portfolio_portfolioid'], ['portfolio.portfolioid'], ),
    sa.PrimaryKeyConstraint('coin_coinid', 'portfolio_portfolioid'),
    info={'bind_key': None}
    )
    op.create_table('user_coin',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('coin_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coin_id'], ['coin.coinid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'coin_id'),
    info={'bind_key': None}
    )
    op.create_table('user_portfolio',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('portfolio_portfolioid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['portfolio_portfolioid'], ['portfolio.portfolioid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'portfolio_portfolioid'),
    info={'bind_key': None}
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_portfolio')
    op.drop_table('user_coin')
    op.drop_table('coin_portfolio')
    op.drop_table('user')
    op.drop_table('portfolio')
    op.drop_table('coin')
    # ### end Alembic commands ###