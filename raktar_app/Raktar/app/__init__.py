from flask import Config, Flask
from config import Config
from app.extensions import db

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Initialize Flask extensions

    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    #Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app