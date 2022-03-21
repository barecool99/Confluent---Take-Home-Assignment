# Confluent---Take-Home-Assignment

Initialise virtual environment
    
  > python -m venv venv

  > venv/Scripts/activate

  > pip install -r requirements.txt


# Assignment Questions:

Experiment with multiple partitions in your topics. How do the number of partitions affect your producer and
consumer applications?

  Producers allocate messages to partitions in a round robin fashion (each message is sent to the next partition in turn). 
  This will in turn balance out the amount of messages sent to each partition and ensure that no single partition is 
  overloaded.
  
  Consumers only read messages from their assigned partitions. If there were 6 partitions and 2 consumers, the partitions
  would be evenly split between the two consumers to read the messages from as efficiently as possible. However, if there
  was 4 partitions and 5 consumers, there would be 1 consumer that would be idling until one of the already assigned consumers
  stops reading messages due to being stopped.


Experiment with the Kafka producer config settings, specifically acks, batch.size and linger.ms. How do these affect
throughput, latency and durability?

  'linger.ms' groups together messages that are being held due to high load. This helps reduce the overall load by as
  messages are being sent grouped together rather than as individual requests. Therefore, this improves the overall
  throughput of the system however, it comes at a cost of adding latency to messages being sent out which can be set
  within the config.

  'acks' is a configuration option to determine when the producer can mark a message being sent as successful. The 
  default option (0) does not require the producer to have an acknowledgement returned to mark a message sent as succesful.
  When 'acks' is set to '1', the producer must await for an acknowledgement to be returned from a topic to mark the 
  message as being succesfully sent. Finally, option 'all' requires the producer to receive an acknowledgement from all
  topics the message has been sent to to return an acknowledgement before marking the message as a success. Using either
  options '1' or 'all' will impact the durability of the system by ensuring that the producer must receive an acknowledgement 
  and therefore cannot mark a message as success before verifying it has been delivered.

  'batch.size' groups together individual messages into grouped messages reducing the number of individual requests being 
  made to the topic/kafka server. This may negatively impact the rate at which messages are sent if the batch size is 
  too small. It may also impact the latency if the batch size is too large as a message may be queued for some time
  until the batch is large enough to be sent off based on the configuration value.


Experiment with the Kafka consumer config settings, how do multiple consumers work together?

  Depending on the # of partitions on the given topic, the consumers will automatically split the partitions that they
  will read the messages from between them. ==> 1 topic has 10 partitions, 2 consumers will split the partitions evenly
  reading meassages from 5 partitions respectively. 


In your consumer application output the message metadata to the console (partition, offset, etc)

  Example console output:
    Consumed event from topic tpc-race-data | value = {"season": "1958", "round": "7", "Races": 
    [{"season": "1958", "round": "7", "url": "http://en.wikipedia.org/wiki/1958_British_Grand_Prix", "raceName": 
    "British Grand Prix", "Circuit": {"circuitId": "silverstone", "url": "http://en.wikipedia.org/wiki/Silverstone_Circuit", 
    "circuitName": "Silverstone Circuit", "Location": {"lat": "52.0786", "long": "-1.01694", "locality": "Silverstone", 
    "country": "UK"}}, "date": "1958-07-19"}]}zn
    Message Metadata >> Offset: 2048 | Partition: 0


Install and connect the Confluent Cloud CLI to your cluster
    
    > confluent login

    > confluent environment use env-00666

    > confluent kafka cluster use lkc-388g5j


Create additional ksqlDB streams and tables
Issues occured when trying to create the ksqlDB streams/tables. No data was being streamed to either process.

Use a managed Connector to sink your messages to an external system
ElasticSearch & Kibana was utilised.
