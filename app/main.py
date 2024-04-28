from fastapi import FastAPI
from app.core.settings import settings
from .api.urls import router
import logging
from contextlib import asynccontextmanager
from app.streaming.admin import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def include_router(app:FastAPI):
    app.include_router(router)
    
@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("STARTUP EVENT")
    try:
        admin_client = Client(
            {
                "bootstrap.servers":settings.KAFKA_BROKER,
                "security.protocol":settings.SECURITY_PROTOCOL,
                "sasl.mechanism":settings.SASL_MECHANISM,
                "sasl.username":settings.SASL_USERNAME,
                "sasl.password":settings.SASL_PASSWORD
            },logger=logger
        )
        topics = ["new_orders","rejected_orders","confirmed_orders","delivering_orders"]
        # admin_client.create_topics(topics)
        admin_client.delete_topics(topics)
        yield
    except Exception as e:
        logger.exception(f"Exception - {e}")

    logger.info("EXIT EVENT")

def start_application():
    app = FastAPI(title=settings.TITLE,version=settings.VERSION,lifespan=lifespan)
    include_router(app)
    return app



app = start_application()