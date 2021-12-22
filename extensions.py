from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import config


def make_celery():
    celery = Celery(
        __name__,
        backend=config.CELERY_RESULT_BACKEND,
        broker=config.CELERY_BROKER_URL,
        include=config.CELERY_INCLUDE
    )
    
    return celery


db = SQLAlchemy()
celery = make_celery()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    db.app = app

    init_celery(app)

    return app


def init_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
