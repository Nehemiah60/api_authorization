from flask import Flask, redirect
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.models import db, Bookmarks
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Check if we are running  test
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DB_URI'),
            JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

        )

    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.route('/<short_url>', methods=['GET'])
    def redirect_to_url(short_url):
        bookmark = Bookmarks.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits += 1
            db.session.commit()
            return redirect(bookmark.url)

    return app