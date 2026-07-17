"""
Package: service

The accounts microservice package. Creates and configures the Flask
application using the application factory pattern.
"""
import logging

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

from service import config
from service.models import db


def create_app(test_config: dict = None) -> Flask:
    """Creates and configures an instance of the Flask application

    Args:
        test_config (dict): configuration overrides used by the test suite
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    if test_config:
        flask_app.config.update(test_config)

    # Security headers (force_https disabled for local development)
    Talisman(flask_app, force_https=False)

    # Cross-Origin Resource Sharing policy: allow all origins on all routes
    CORS(flask_app, resources={r"/*": {"origins": "*"}})

    db.init_app(flask_app)

    # Import must happen after db is defined to avoid circular imports
    from service.routes import bp  # pylint: disable=import-outside-toplevel

    flask_app.register_blueprint(bp)

    with flask_app.app_context():
        db.create_all()

    flask_app.logger.setLevel(logging.INFO)
    flask_app.logger.info("Service initialized!")
    return flask_app


# Application instance used by gunicorn (service:app)
app = create_app()
