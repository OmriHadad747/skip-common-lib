from pydantic import BaseSettings, BaseModel, validate_arguments


class ProductionSettings(BaseSettings):
    environment: str = "production"
    debug: bool = False
    testing: bool = False

    mongo_uri: str
    mongo_db_name = "skip-db"
    redis_uri: str

    freelancer_finder_url: str
    
    customers_collection_name: str
    freelancers_collection_name: str
    jobs_collection_name: str

    firebase_sak: str

    class Config:
        env_prefix = "prod_"
        env_file = ".env"


class DevelopmentSettings(ProductionSettings):
    environment: str = "development"
    debug: bool = True
    testing: bool = False

    mongo_uri: str = "mongodb://localhost:27017/"
    mongo_db_name = "skip-db-dev"
    redis_uri: str = "redis://localhost:6379/0"

    customers_collection_name: str = "Customers"
    freelancers_collection_name: str = "Freelancers"
    jobs_collection_name: str = "Jobs"

    freelancer_finder_url: str = "http://localhost:8001"

    class Config: 
        env_prefix = "dev_"


class DockerDevelopmentSettings(DevelopmentSettings):
    mongo_uri: str = "mongodb://mongodb:27017/"
    redis_uri: str = "redis://redis:6379/0"

    freelancer_finder_url: str = "http://skip-freelancer-finder:8001"


class TestSettings(ProductionSettings):
    environment: str = "testing"
    debug: bool = False
    testing: bool = True

    mongo_uri: str = "mongodb://localhost:27017/"
    mongo_db_name = "skip-db-test"
    redis_uri: str = "redis://localhost:6379/0"

    customers_collection_name: str = "Customers-test"
    freelancers_collection_name: str = "Freelancers-test"
    jobs_collection_name: str = "Jobs-test"


class AppSettings(BaseModel):
    setting: ProductionSettings | DevelopmentSettings | DockerDevelopmentSettings | TestSettings = None

    def init(self, env_settings: ProductionSettings | DevelopmentSettings | DockerDevelopmentSettings | TestSettings):
        self.setting = env_settings()

settings = AppSettings()