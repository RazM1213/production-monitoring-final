import json
import logging
from typing import List

import coloredlogs
from kafka import KafkaProducer

from consts.formats import ENCODE_FORMAT
from models.elastic.elastic_report_response_doc import ElasticReportResponseDoc
from publish.i_publisher import IPublisher
from utils.encoder.json_encoder import Encoder


class KafkaPublisher(IPublisher):
    def __init__(self, topic: str, bootstrap_servers: List[str]):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def publish(self, report: ElasticReportResponseDoc):
        self.producer.send(topic=self.topic, value=str(json.dumps(report, cls=Encoder)).encode(ENCODE_FORMAT))
        coloredlogs.install()
        logging.info("Published Message to Kafka topic{}:\n {}".format(str(json.dumps(report, cls=Encoder)).encode(ENCODE_FORMAT), self.topic))
