from . import db
from flask_login import UserMixin


user_portfolio = db.Table('user_portfolio',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('portfolio_portfolioid', db.Integer, db.ForeignKey('portfolio.portfolioid'), primary_key=True)
)

user_coin = db.Table('user_coin',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('coin_id', db.Integer, db.ForeignKey('coin.coinid'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)
)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True, nullable=False)
    password=db.Column(db.String(150),unique=True, nullable=False)
    email=db.Column(db.String(150),unique=True, nullable=False)
    portfolios = db.relationship(
        'Portfolio',
        secondary=user_portfolio,
        back_populates='users',
        lazy='dynamic'
    )

    
    coins = db.relationship('Coin', secondary=user_coin, back_populates='users')



# Association Table
coin_portfolio = db.Table('coin_portfolio',
    db.Column('coin_coinid', db.Integer, db.ForeignKey('coin.coinid'), primary_key=True),
    db.Column('portfolio_portfolioid', db.Integer, db.ForeignKey('portfolio.portfolioid'), primary_key=True),
    
)



class Coin(db.Model):
    coinid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    change24hrpercentage=db.Column(db.Float, nullable=False)
    portfolios = db.relationship(
        'Portfolio',
        secondary=coin_portfolio,
        back_populates='coins'
    )
    users = db.relationship('User', secondary=user_coin, back_populates='coins')



class Portfolio(db.Model):
    portfolioid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    coins = db.relationship(
        'Coin',
        secondary=coin_portfolio,
        back_populates='portfolios',
        lazy='dynamic'
    )
    users = db.relationship(
        'User',
        secondary=user_portfolio,
        back_populates='portfolios',
        lazy='dynamic'
    )