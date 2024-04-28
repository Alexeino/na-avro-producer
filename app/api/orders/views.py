from fastapi import APIRouter
from app.core.settings import settings
from .schemas import OrderSchema
from confluent_kafka.serialization import StringSerializer, SerializationContext,MessageField
from app.streaming.producer import AvroClient
import logging
import json

logging.basicConfig(level=logging.INFO)

def order_to_dict(order:OrderSchema,ctx)-> dict:
    data =  order.model_dump_json()
    return json.loads(data)

client = AvroClient(
    topic_name="new_orders",
    sr_config={
        "sr_url":settings.SCHEMA_REGISTRY_URL,
        "sr_api_key":settings.SCHEMA_REGISTRY_API_KEY,
        "sr_secret_key":settings.SCHEMA_REGISTRY_SECRET_KEY
    },
    schema_name="orders_v1.avsc",
    model_converter=order_to_dict,
    pr_config={
            "bootstrap.servers":settings.KAFKA_BROKER,
            "security.protocol":settings.SECURITY_PROTOCOL,
            "sasl.mechanism":settings.SASL_MECHANISM,
            "sasl.username":settings.SASL_USERNAME,
            "sasl.password":settings.SASL_PASSWORD
            }
    )


order_router = APIRouter()
string_serializer = StringSerializer('utf_8')

@order_router.post("/create")
async def order_create(order:OrderSchema):
    try:
        avro_serializer = client.create_avro_serializer()
        client.producer.produce(
            topic = client.topic_name,
            key = string_serializer(str(order.order_id)),
            value = avro_serializer(order, SerializationContext(client.topic_name, MessageField.VALUE)),
            on_delivery=client.delivery_report
        )
        logging.info(f"Successfully Produces message {order}")
    except Exception as e:
        logging.exception(f"Exception occurred",exc_info=e)
    return order.model_dump()

