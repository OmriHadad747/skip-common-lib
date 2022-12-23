from motor import motor_asyncio

from skip_common_lib.settings import app_settings as s


db: motor_asyncio.AsyncIOMotorDatabase = motor_asyncio.AsyncIOMotorClient(f"{s.setting.mongo_uri}")[
    s.setting.db_name
]
_freelancers = s.setting.freelancers_collection_name
_customers = s.setting.customers_collection_name
_jobs = s.setting.jobs_collection_name
