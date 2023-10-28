# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts - Youssef Alaoui - Aydan Guliyeva


from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
photos = UploadSet('photos', IMAGES)


def create_app(config_classname):
    """
    Initialise the Flask application.
    :type config_classname: Specifies the configuration class :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    # Initialise
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    configure_uploads(app, photos)

    with app.app_context():
        from flask_app.models import User, Profile, Posts, Comments, Comment_Likes
        db.create_all()

        # Uncomment the following if you want to experiment with reflection
        # db.Model.metadata.reflect(bind=db.engine)

        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

    from flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from flask_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from flask_app.dash_html_test.routes import dash_html_bp
    app.register_blueprint(dash_html_bp)

    from flask_app.Profile_and_Account.routes import Profile_and_Account_bp
    app.register_blueprint(Profile_and_Account_bp)

    return app
