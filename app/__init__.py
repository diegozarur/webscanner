import os
from celery import Celery
from flask import Flask
from importlib import import_module
from flask_cors import CORS
import logging
from config import Config

celery = Celery(
    __name__,
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=['app.views.scanning.tasks']
)


def register_blueprints(flask_app):
    for module_name in ['scanning']:
        module = import_module('app.views.{}.routes'.format(module_name))
        flask_app.register_blueprint(module.blueprint)


def create_app(config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)

    register_blueprints(flask_app)

    CORS(flask_app, resources={r"/*": {"origins": "*"}})

    celery.conf.update(flask_app.config)

    UPLOAD_DIRECTORY = f"{flask_app.root_path}/api_uploaded_files"

    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    flask_app.config["UPLOAD_FOLDER"] = UPLOAD_DIRECTORY

    return flask_app


def make_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('webscanner.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', datefmt="%d/%m/%Y %I:%M:%S %p")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
