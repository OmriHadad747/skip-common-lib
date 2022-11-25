from firebase_admin import credentials
from redis import Redis

from ..settings import settings as s


firebase_admin_creds = credentials.Certificate(s.setting.firebase_sak)

redis = Redis.from_url(s.setting.redis_uri)
print(f"from queue {redis.rpop('new-jobs')}")   # TODO find a better way to clear the queue