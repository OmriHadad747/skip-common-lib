from firebase_admin import credentials
from redis import Redis
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
from flask import current_app as app

# TODO find a way to init only what is neccessary

firebase_admin_creds = credentials.Certificate(app.config["FIREBASE_SERVICE_ACCOUNT"])

redis = Redis(
    host=app.config["REDIS_HOST"],
    port=app.config["REDIS_PORT"],
    db=app.config["REDIS_DB"],
    decode_responses=True,
)
# TODO find a better way to clear the queue
print(f"from queue {redis.rpop('new-jobs')}")

scheduler = APScheduler()

jwt = JWTManager()
