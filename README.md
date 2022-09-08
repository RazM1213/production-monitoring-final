# production-monitoring

## Problem Definition:

Nowadays, the industry consists of many monitoring services systems to choose from.
A good example is Elastic Heartbeat - which, according to Elastic "asks the simple question: Are you alive? "
AND THAT'S IT.
What if we as developers or QA, want to get more valuable data out of the monitoring process ?
There are a lot more questions which have to be answered, even if the service is up and running.

## PM's responsibility:

Send sanity HTTP requests to the tested API, get the responses, create reports and send them in a queue to further use.

## The monitoring process:

1. Send sanity HTTP requests asynchronously to the tested API - once and every hour
2. Get the responses from the tested API
3. Aggregate and transform the responses - to use valuable data from them, and enrich it
4. Create a report for each and every tested route
5. Produce the reports to a Kafka topic
6. Write the reports to Elasticsearch using Logstash - by configuring it to read from kafka and write to Elasticsearch
7. Create a dashboard by using Kibana