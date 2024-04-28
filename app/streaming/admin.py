from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException, KafkaError
from logging import Logger

class Client:
    def __init__(self,config:dict, logger: Logger):
        self.client = AdminClient(config)
        self.logger = logger
    
    def create_topics(self,topics:list):
        
        new_topics = [NewTopic(topic,num_partitions=3,replication_factor=3) for topic in topics]

        futures = self.client.create_topics(new_topics)

        for topic, future in futures.items():
            try:
                future.result()
                self.logger.info(f"Topic {topic} created.")
            except KafkaException as e:
                if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                    self.logger.warning(f"Topic {topic} already exists.")
            except Exception as e:
                self.logger.exception(f"Exception at create_topics - {e}")


    def delete_topics(self,topics:list):
        # topics_to_delete = [NewTopic(topic,num_partitions=3,replication_factor=3) for topic in topics]
        
        futures = self.client.delete_topics(topics,operation_timeout=20)
        for topic, future in futures.items():
            try:
                future.result()
                self.logger.info(f"Topic {topic} deleted.")
            except KafkaException as e:
                if e.args[0].code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    self.logger.warning(f"Topic {topic} does not exists.")
            except Exception as e:
                self.logger.exception(f"Exception at delte_topics - {e}")