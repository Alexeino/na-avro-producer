from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import os
from typing import Callable

class AvroClient:
    def __init__(self,topic_name,sr_config,schema_name,model_converter:Callable[...,dict],pr_config:dict):
        self.sr_client = SchemaRegistryClient(
            {
                "url":sr_config["sr_url"],
                "basic.auth.user.info":f"{sr_config['sr_api_key']}:{sr_config['sr_secret_key']}"
            }
        )
    
        self.topic_name = topic_name
        self.schema_name = schema_name
        self.model_converter = model_converter
        self.producer = Producer({
            "bootstrap.servers":pr_config["bootstrap.servers"],
            "security.protocol":pr_config["security.protocol"],
            "sasl.mechanism":pr_config["sasl.mechanism"],
            "sasl.username":pr_config["sasl.username"],
            "sasl.password":pr_config["sasl.password"],
        })
        
    def create_avro_serializer(self,sr_client: SchemaRegistryClient=None):
        path = os.path.realpath(os.path.dirname(__file__))

        with open(f"{path}/avro/{self.schema_name}") as file:
            schema_str = file.read()

        return AvroSerializer(
            self.sr_client,
            schema_str,
            self.model_converter
        )
        
    def delivery_report(self,err,msg):
        if err is not None:
            print("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        print('User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))