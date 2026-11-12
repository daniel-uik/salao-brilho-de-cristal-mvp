import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    """Application factory for the Salao Brilho de Cristal MVP."""
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    default_db = f"sqlite:///{os.path.join(basedir, 'salao.db')}"

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-brilho-de-cristal'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', default_db),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
