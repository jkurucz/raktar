from apiflask import APIFlask
from config import Config
from app.extensions import db
from app.models import *

def create_app(config_class = Config):
    #app = Flask(__name__)
    app = APIFlask(__name__, json_errors = True, 
               title="Raktár API",
               docs_path="/swagger")
    app.config.from_object(config_class)
    
    #Initialize Flask extensions

    db.init_app(app)


    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    #Register blueprints
    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix='/api')

    return app