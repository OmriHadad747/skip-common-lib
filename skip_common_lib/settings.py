from pydantic import BaseSettings, BaseModel, MongoDsn, RedisDsn


class ProductionSettings(BaseSettings):
    environment: str = "production"
    debug: bool = False
    testing: bool = False

    mongo_uri: MongoDsn
    db_name: str
    
    redis_uri: RedisDsn

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

    customers_collection_name: str = "Customers"
    freelancers_collection_name: str = "Freelancers"
    jobs_collection_name: str = "Jobs"

    freelancer_finder_url: str = "http://localhost:8001"

    class Config:
        env_prefix = "dev_"


class DockerDevelopmentSettings(DevelopmentSettings):
    freelancer_finder_url: str = "http://skip-freelancer-finder:8001"

    class Config:
        env_prefix = "docker_"


class TestSettings(ProductionSettings):
    environment: str = "testing"
    debug: bool = False
    testing: bool = True

    mongo_uri: MongoDsn = "mongodb://localhost:27017/"
    db_name: str = "skip-db-test"
    customers_collection_name: str = "Customers-test"
    freelancers_collection_name: str = "Freelancers-test"
    jobs_collection_name: str = "Jobs-test"

    redis_uri: RedisDsn = "redis://localhost:6379/0"


class AppSettings(BaseModel):
    setting: ProductionSettings | DevelopmentSettings | DockerDevelopmentSettings | TestSettings = (
        None
    )

    def init(
        self,
        env_settings: ProductionSettings
        | DevelopmentSettings
        | DockerDevelopmentSettings
        | TestSettings,
    ):
        self.setting = env_settings()


app_settings = AppSettings()
