from flask import Flask
from skip_common_lib import config


def create_app(app_config: config.BaseConfig) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config)

    with app.app_context():
        from skip_common_lib import database
        database.mongo.init_app(app)

        import playground

        return app
