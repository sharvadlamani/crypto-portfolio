from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_migrate import Migrate

from flask_cors import CORS  # Import CORS



db=SQLAlchemy()
login_manager = LoginManager()
def create_app():
    app=Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)
    from .models import User as User
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}},supports_credentials=True)  # Allow all origins, adjust as needed

    from app.views import main_bp
    app.register_blueprint(main_bp)

    from app.portfolio import portfolio_bp
    app.register_blueprint(portfolio_bp)


    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler()
    from .coins import get_crypto_details
    from .models import Coin
        
    def add_new_coin(coin):
        existing_coin = Coin.query.filter_by(symbol=coin['symbol']).first()
        
        if existing_coin:
            # Coin already exists, so you may want to update its details instead
            return False
        
        new_coin = Coin(
            symbol=coin['symbol'],
            name=coin['name'],
            price=coin['price'], # Example additional field
            change24hrpercentage=coin['change24hrpercentage']
        )

        db.session.add(new_coin)
        db.session.commit()
        
        return True



    def update_coin_details():

        coins_data = get_crypto_details()

        if not coins_data:
            return
        
        for coin in coins_data:
            added = add_new_coin(coin)
            if not added:
                #update the price
                existing_coin = Coin.query.filter_by(symbol=coin['symbol']).first()
                existing_coin.price=coin['price']
                existing_coin.change24hrpercentage=coin['change24hrpercentage']

                db.session.commit()

    def update_coin():
        with app.app_context():
            # Import your update_coin_details function here to avoid circular imports
            update_coin_details()


    # Add job to run update_coin_details every minute
    scheduler.add_job(update_coin, 'interval', seconds=20)

    # Start the scheduler
    scheduler.start()

    # Ensure to handle the scheduler's shutdown gracefully
    import atexit
    atexit.register(lambda: scheduler.shutdown())

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app