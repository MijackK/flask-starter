from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
mail = Mail()
limiter = Limiter(get_remote_address)
# proxy = ProxyFix(x_for=1, x_proto=1, x_host=1, x_prefix=1)


def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.config.from_object("config.Config")

    CORS(app)

    # connect to database
    db.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    # tell flask its behind a proxy
    if not app.config["DEBUG"]:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from authentication.routes import authentication


    app.register_blueprint(authentication)

    @app.route("/", methods=["GET"])
    def index():
        return "flask backend up and running"


    @app.route("/init", methods=["POST"])
    def hello_init():
        from authentication.models import User
        from werkzeug.security import generate_password_hash
        from flask import current_app

        if not current_app.config["DEBUG"]:
            db.create_all()
            db.session.commit()
            return "database tables created"

        db.drop_all()
        db.create_all()
        # make admin account
        admin = User(
            username="admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin"),
        )
        admin.admin = True
        admin.verify = True
        db.session.add(admin)
        # commit changes
        db.session.commit()
        return "initialized"

    return app



