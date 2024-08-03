from flask import Blueprint, request, jsonify
from .models import User , Portfolio, Coin
from . import db
from flask_login import login_required
from flask_login import current_user

portfolio_bp=Blueprint('portfolio', __name__)



portfolios = {}
@portfolio_bp.route('/portfolio/viewall', methods=['GET'])
@login_required
def get_user_portfolios_id_name():
    user = User.query.filter_by(username=current_user.username).first()
    portfolios=user.portfolios
    mylist=[]
    for portfolio in portfolios:
        mylist.append([portfolio.portfolioid,portfolio.title])
    message={'portfolios':mylist,"category":"success"}
    return jsonify(message,201)


#user can create portfolio
portfolios = {}
@portfolio_bp.route('/portfolio/create/<string:portfolioname>', methods=['GET'])
@login_required
def create_portfolio(portfolioname):
    user = User.query.filter_by(username=current_user.username).first()
    portfolio=Portfolio(title=portfolioname)
    
    db.session.add(portfolio)
    db.session.commit()
    portfolio=Portfolio.query.filter_by(title=portfolioname).first()
    portfolio.users.append(user)
    db.session.commit()
    return jsonify({
        "message":"Created Portfolio",
        "category":"success"
    },201)



@portfolio_bp.route('/portfolio/delete/<string:portfolioname>', methods=['DELETE'])
@login_required
def delete_portfolio(portfolioname):
    # Query for the portfolio by its title
    portfolio = Portfolio.query.filter_by(title=portfolioname).first()

    if not portfolio:
        # If the portfolio does not exist, return an error response
        return jsonify({
            "message": "Portfolio not found",
            "category": "error"
        }), 404

    # Ensure the portfolio is associated with the current user
    if current_user not in portfolio.users:
        # If the current user is not associated with the portfolio, return an error response
        return jsonify({
            "message": "You are not authorized to delete this portfolio",
            "category": "error"
        }), 403

    # Remove the portfolio from the current user's list of portfolios
    portfolio.users.remove(current_user)

    # If there are no users associated with the portfolio, delete it from the database
    if not portfolio.users:
        db.session.delete(portfolio)

    db.session.commit()

    return jsonify({
        "message": "Deleted Portfolio",
        "category": "success"
    }), 200



# add coins in portfolio
@portfolio_bp.route('/portfolio/add_coin/<string:portfolioname>/<string:coin_symbol>', methods=['POST'])
@login_required
def add_coin_to_portfolio(portfolioname, coin_symbol):
    portfolio = Portfolio.query.filter_by(title=portfolioname).first()

    if not portfolio:
        return jsonify({
            "message": "Portfolio not found",
            "category": "error"
        }), 404

    if current_user not in portfolio.users:
        return jsonify({
            "message": "You are not authorized to modify this portfolio",
            "category": "error"
        }), 403

    coin = Coin.query.filter_by(symbol=coin_symbol).first()

    if not coin:
        return jsonify({
            "message": "Coin not found",
            "category": "error"
        }), 404

    portfolio.coins.append(coin)
    db.session.commit()

    return jsonify({
        "message": f"Added {coin_symbol} to {portfolioname}",
        "category": "success"
    }), 200


#delete coins in portfolio
@portfolio_bp.route('/portfolio/delete_coin/<string:portfolioname>/<string:coin_symbol>', methods=['DELETE'])
@login_required
def delete_coin_from_portfolio(portfolioname, coin_symbol):
    portfolio = Portfolio.query.filter_by(title=portfolioname).first()

    if not portfolio:
        return jsonify({
            "message": "Portfolio not found",
            "category": "error"
        }), 404

    if current_user not in portfolio.users:
        return jsonify({
            "message": "You are not authorized to modify this portfolio",
            "category": "error"
        }), 403

    coin = Coin.query.filter_by(symbol=coin_symbol).first()

    if not coin:
        return jsonify({
            "message": "Coin not found",
            "category": "error"
        }), 404

    portfolio.coins.remove(coin)
    db.session.commit()

    return jsonify({
        "message": f"Deleted {coin_symbol} from {portfolioname}",
        "category": "success"
    }), 200


#get all portfolio coins
@portfolio_bp.route('/portfolio/<string:portfolioname>/coins', methods=['GET'])
@login_required
def get_all_coins_in_portfolio(portfolioname):
    portfolio = Portfolio.query.filter_by(title=portfolioname).first()

    if not portfolio:
        return jsonify({
            "message": "Portfolio not found",
            "category": "error"
        }), 404

    if current_user not in portfolio.users:
        return jsonify({
            "message": "You are not authorized to view this portfolio",
            "category": "error"
        }), 403

    coins = portfolio.coins
    coins_list = []
    for coin in coins:
        coins_list.append({
            "name": coin.name,
            "symbol": coin.symbol,
            "price": coin.price,
            "change24hrpercentage": coin.change24hrpercentage
        })

    return jsonify({
        "portfolio": portfolioname,
        "coins": coins_list,
        "category": "success"
    }), 200

@portfolio_bp.route('/coins/all', methods=['GET'])
@login_required
def all_coins():
    coins = Coin.query.all()
    coin_list = [{'id': coin.id, 'name': coin.name, 'symbol': coin.symbol, 'price': coin.price,"change24hrpercentage": coin.change24hrpercentage} for coin in coins]
    return jsonify(coin_list), 200