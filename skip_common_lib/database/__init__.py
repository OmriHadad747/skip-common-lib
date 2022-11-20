from flask_pymongo import PyMongo as FlaskPymongo
from flask_pymongo import wrappers
from werkzeug.local import LocalProxy
from flask import current_app, g


mongo = FlaskPymongo()


def get_dbs() -> wrappers.Collection:
    if "database" not in g:
        g.database = FlaskPymongo(current_app, uuidRepresentation="standard")
    return g.database.db


db: wrappers.Collection = LocalProxy(get_dbs)
_freelancers = current_app.config["FREELANCER_COLLECTION"]
_customers = current_app.config["CUSTOMER_COLLECTION"]
_jobs = current_app.config["JOB_COLLECTION"]
