import todo_api_monitor_request_mapping
from config.config import TOPIC, BOOTSTRAP_SERVERS
from monitor import Monitor
from publish.kafka.kafka_publisher import KafkaPublisher


def main():
    monitor = Monitor(
        todo_api_monitor_request_mapping.REQUESTS,
        KafkaPublisher(topic=TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    )

    monitor.start()


if __name__ == "__main__":
    main()
