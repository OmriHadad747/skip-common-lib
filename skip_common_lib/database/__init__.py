from pymongo import MongoClient

from skip_common_lib.settings import settings as s

db = MongoClient(f"{s.setting.mongo_uri}")[s.setting.mongo_db_name]
_freelancers = s.setting.freelancers_collection_name
_customers = s.setting.customers_collection_name
_jobs = s.setting.jobs_collection_name
