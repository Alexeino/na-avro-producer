from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
from typing import ClassVar

env_path = Path(__file__).resolve().parent.parent.parent / 'params.env'
load_dotenv(env_path)

class Settings(BaseSettings):
    TITLE: str = "Food Delivery System"
    VERSION: str = "0.1"

    KAFKA_BROKER:str
    SECURITY_PROTOCOL:str
    SASL_MECHANISM:str
    SASL_USERNAME:str
    SASL_PASSWORD:str
    SCHEMA_REGISTRY_URL:str
    SCHEMA_REGISTRY_API_KEY:str
    SCHEMA_REGISTRY_SECRET_KEY:str
    SESSION_TIMEOUT:str
    
    SCHEMA_REGISTRY_NAME: str = "orders-value"
    AVRO_PATH: str  = str(Path(__file__).parent.parent / 'avro/orders_v1.avsc')
    
    class Config:
        env_path = env_path
        
settings = Settings()
print(settings.AVRO_PATH)

if __name__ == "__main__":
    print(settings.__dict__)