# azure-eventhub-kafka-streaming

## Part 1: Customer Use Cases 

- Augment current batch processing with streaming solution for n-number of sources
- Understand streaming services - Azure EventHubs, Azure EventGrid, Azure ServiceBus, etc
- Understand Azure and Kafka, and Azure EventHubs roadmap re: Kafka-like features
- Understand Azure Stream Analytics
- Use Azure Data LakeGen2 as an event sink
- Explore Azure Databricks with Spark Streaming

---

## Part 2: Azure Event Processing Services

- [See the Azure Documentation](https://docs.microsoft.com/en-us/azure/?product=all)

### Azure PaaS 

- [Azure EventHubs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-about)
  - [Azure EventHubs w/Kafka](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-for-kafka-ecosystem-overview)
  - [Azure EventHubs w/Capture](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-enable-through-portal)
- [Azure IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/about-iot-hub)
- [Azure HDInsight w/Kafka](https://docs.microsoft.com/en-us/azure/hdinsight/kafka/apache-kafka-introduction)
- [Azure Service Bus](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview)
- [Azure Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/overview)
- [Azure Stream Analytics](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction)
- [Azure Machine Learning](https://docs.microsoft.com/en-us/azure/stream-analytics/machine-learning-udf)
- [Azure Databricks with Spark Streaming](https://docs.microsoft.com/en-us/azure/azure-databricks/databricks-stream-from-eventhubs)
- [Azure Synapse with Spark Streaming](https://docs.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-overview-what-is) (Preview)
- [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview)
- [Azure CosmosDB](https://docs.microsoft.com/en-us/azure/cosmos-db/introduction)

### 

- Marketplace Offerings - ActiveMQ, RabbitMQ, etc 

---

## Part 3: Demonstration

<p align="center">
  <img src="img/azure-streaming-demo.png">
</p>

Demo app consists of (the solid lines in the diagram above):
1) Azure Command-Line Interface (CLI) program **az**
2) Azure EventHub with Kafka Enabled
3) Azure Blob Storage for EventHub message Capture
4) Azure Stream Analytics to Consume to EventHub
5) Azure CosmosDB - Sink for Azure Stream Analytics
   - Queries
   - Geo Queries (GeoJSON)
6) Azure Datalake Gen2 - Sink for Azure Stream Analytics
7) Three different EventHub Message Producers
   - Python Kafka Protocol Message Producer
   - Python Native Protocol Message Producer
   - DotNet Core Native Protocol Message Producer
8) (TODO) Azure Databricks - Alternative EventHub stream consumer

---

### Alternative EventHub Pipeline

EventHubs and Azure Functions can be **pipelined** for functionality similar to **Kafka Streams** Java code.

<p align="center">
  <img src="img/eh-pipeline.png">
</p>

### Provisioning the Azure Resources for this Demonstration

You can provision Azure Resources in at least four ways:
- The Azure Portal Web Application (portal.azure.com)
- Azure Resource Manager (ARM) templates
- PowerShell cmdlets
- Azure Command-Line Interface (CLI) program **az**
  - See https://docs.microsoft.com/en-us/cli/azure/what-is-azure-cli?view=azure-cli-latest

This demonstration uses the Azure CLI.

See the bash/az scripts in the **automation/az/** directory.
Edit file **env.sh** per your preferred Azure region, resource group, resource names,
and other service configuration.

Execute each of these scripts in turn:

```
$ cd automation/az
$ mkdir out

$ ./extensions.sh install        <-- installs extensions to the az cli program
$ ./eventhubs.sh recreate        <-- provisions eventhubs with kafka api enabled, with dev hub
$ ./adl.sh create                <-- provisions datalake gen 2
$ ./storage.sh create            <-- provisions blob storage
$ ./cosmos_sql.sh create         <-- provisions cosmosdb with sql api and events collection
$ ./stream_analytics.sh create   <-- provisions an empty stream analytics account (no code)
  - or -
$ ./provision_all.sh             <-- provision all of the above
```

#### Provisioning an Azure EventHubs account to enable Kafka

Script **eventhubs.sh** specifies **--enable-kafka** to be true.

Note: This EventHub instance will support **both** types of clients - 
**Kafka API** and the **Microsoft SDKs**.

```
    az eventhubs namespace create --help   <-- help content is available for all commands at all levels

    az eventhubs namespace create \
        --name $eventhubs_namespace \
        --resource-group $eventhubs_rg \
        --subscription $subscription \
        --location $eventhubs_region \
        --sku $eventhubs_sku \
        --enable-kafka $eventhubs_enable_kafka \
        --enable-auto-inflate $eventhubs_enable_auto_inflate \
        --maximum-throughput-units $eventhubs_max_tu \
        > out/eventhubs_namespace_create.json
```

#### More Detail on Azure EventHubs

- Maximum size of Event Hubs event is 256KB (Basic Tier) or 1MB (Standard Tier)
- The number of **partitions** is specified at creation, up to 32
- Use Partitions for more downstream/reader parallelism
- Use a 1:1 correlation between partitions and Throughput Units (TU)
- A single Throughput Unit (TU) lets you:
  - Ingress: Up to 1 MB per second or 1000 events per second (whichever comes first)
  - Egress: Up to 2 MB per second or 4096 events per second
- [Features](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-features)
- [Partition Keys](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-features#event-publishers)
- [Partitions](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-features#partitions)
- [Consumer Groups](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-features#event-consumers)
- [Throughput Units](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-scalability)
- [Scaling](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-scalability)
- [Auto Inflate](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-auto-inflate)
- [Pricing](https://azure.microsoft.com/en-us/pricing/details/event-hubs/)

#### CosmosDB Time-to-Live

TTL can optionally be set in CosmosDB, for example:

```
    --ttl 86400   (optional, in seconds, 60 * 60 * 24 = 86400, or 24 hours)
```

### Configure EventHub Message Capture

Azure EventHub messages can optionally and automatically be captured to Azure Blob storage, 
Azure Data Lake Storage Gen1, or Azure Data Lake Storage Gen2.
See https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-enable-through-portal

The output data format is **avro**.

This can be configured in Azure Portal in your EventHub account as shown here:

<p align="center">
  <img src="img/eventhub-capture-to-storage.png">
</p>

### Create the Azure Stream Analytics Job

Easily consume the EventHub stream of data, and save it to **both** CosmosDB and Data Lake
with only two lines of code.  Simply define the **input (eventhub)** and the **outputs (adl, cosmos)**,
then define the **Job** in a SQL-like syntax:

```
SELECT * INTO adl FROM eventhub
SELECT * INTO cosmos FROM eventhub
```
<p align="center">
  <img src="img/stream-analytics-job.png">
</p>

#### JavaScript User-Defined Functions

- [UDFs](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-javascript-user-defined-functions)

#### JavaScript User-Defined Aggregates & TumblingWindows

- [Aggregates](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-javascript-user-defined-aggregates)

#### Integrate with Azure Machine Learning

- [AML](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-machine-learning-integration-tutorial)

---

### Client Computer Setup

#### Environment Variables

Set the following three environment variables per your EventHub keys in Azure Portal.
Example values are shown.
```
AZURE_STREAMPOC_EVENTHUB_CONN_STRING="Endpoint=sb://cjoakimstreameh.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<secret>"
AZURE_STREAMPOC_EVENTHUB_NAMESPACE=cjoakimstreameh
AZURE_STREAMPOC_EVENTHUB_HUBNAME=dev
```

#### Create Python Virtual Environment

Linux and MacOS:
```
$ cd py
$ ./venv.sh create 
$ source bin/activate
```

Windows:
```
$ cd py
$ .\venv.ps1
```

#### Send messages to EventHub using the Kafka Producer API

Event Hubs supports **Apache Kafka protocol 1.0 and later**, and works with your existing Kafka applications, including MirrorMaker.

The following sends 100 messages in a randomized sequence, with Python and the **confluent-kafka**
library on PyPI.

```
$ python eventhub_kafka.py 1 100

...
sending message: {"location": {"type": "Point", "coordinates": [-80.733927, 35.303614]}, "postal_cd": "28223", "country_cd": "US", "city_name": "Charlotte", "state_abbrv": "NC", "latitude": 35.303614, "longitude": -80.733927, "pk": "28223", "seq": 1, "timestamp": "2020-06-25 15:46:20", "epoch": 1593099980, "sender": "python_kafka_sdk"}
Message delivered to; topic: dev, partition: 0, offset: 248
...
```

Likewise, you can use the **Microsoft SDK** to send messages to the same EventHub with the
native EventHub protocol rather than the Kafka protocol.  This uses the **azure-eventhub**
library on PyPI.

```
$ python eventhub_sdk.py producer 1 100

...
sending message: {"location": {"type": "Point", "coordinates": [-82.5545, 35.6006]}, "postal_cd": "28816", "country_cd": "US", "city_name": "Asheville", "state_abbrv": "NC", "latitude": 35.6006, "longitude": -82.5545, "pk": "28816", "seq": 1, "timestamp": "2020-06-25 15:47:35", "epoch": 1593100055, "sender": "python_ms_sdk"}
...
```

See file **py/data/nc_zipcodes.json** in this repo which contains the demonstration dataset - 
North Carolina postal codes.  These raw messages are augmented by the Python Kafka Producer program
to add pk, seq, timestamp, and epoch attributes.

```
  {
    "location": {
      "type": "Point",
      "coordinates": [
        -80.8433,
        35.5095
      ]
    },
    "postal_cd": "28035",
    "country_cd": "US",
    "city_name": "Davidson",
    "state_abbrv": "NC",
    "latitude": 35.5095,
    "longitude": -80.8433
  },
```

#### But wait, .Net Core, too

```
$ cd dotnet
$ cd EventHubConsoleApp 

$ dotnet --version
3.1.301

$ dotnet build
Build succeeded.

$ dotnet run true 10 
...
Sending message batch of 10
The batch of messages has been sent
Query CosmosDB with: SELECT * FROM c where c.sender = 'dotnet_core_sdk' and c.epoch >= 1593718632
```

### Query the Messages in CosmosDB

Syntax: https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-getting-started

Count the Documents in a container:
```
SELECT VALUE COUNT(1) FROM c
```

Query just one Document:
```
SELECT TOP 1 * FROM c
```

Query by epoch time sent and sender attributes:
```
select * FROM c where c.epoch >= 1593099980 and c.sender = 'python_kafka_sdk'
select * FROM c where c.epoch >= 1593099980 and c.sender = 'python_ms_sdk'

select c.id, c.city_name, c.sender FROM c where c.epoch > 1593099980
```

Spatial/Geo Query, -78.639090, 35.780034 is the North Carolina State Capitol building:
```
SELECT * from c WHERE ST_DISTANCE(c.location, {'type': 'Point', 'coordinates':[-78.639090,35.780034]}) < 10000

SELECT c.postal_cd, c.city_name, c.location from c WHERE ST_DISTANCE(c.location, {'type': 'Point', 'coordinates':[-78.639090,35.780034]}) < 10000

SELECT DISTINCT VALUE c.city_name from c WHERE ST_DISTANCE(c.location, {'type': 'Point', 'coordinates':[-78.639090,35.780034]}) < 10000
```

<p align="center">
  <img src="img/cosmosdb-query-of-events.png">
</p>


### Use the Desktop Azure Storage Explorer App to see the Data

Similar to Windows Explorer - but for Blobs, DataLake, and CosmosDB.  You can upload, download, delete.

[Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)

<p align="center">
  <img src="img/azure-storage-explorer.png">
</p>

### Display the Messages and Schema in an EventHub Avro file

Download an avro file from Azure Blob Storage (i.e. - data/54.avro).
See **avro.py** in the py/ directory.

```
$ python avro.py data/24.avro

Displaying the messages in Avro file: data/24.avro

{'SequenceNumber': 252, 'Offset': '4295015048', 'EnqueuedTimeUtc': '6/25/2020 3:47:29 PM', 'SystemProperties': {}, 'Properties': {}, 'Body': b'{"location": {"type": "Point", "coordinates": [-76.766436, 34.738947]}, "postal_cd": "28557", "country_cd": "US", "city_name": "Morehead City", "state_abbrv": "NC", "latitude": 34.738947, "longitude": -76.766436, "pk": "28557", "seq": 1, "timestamp": "2020-06-25 15:47:27", "epoch": 1593100047, "sender": "python_ms_sdk"}'}

{'SequenceNumber': 253, 'Offset': '4295015424', 'EnqueuedTimeUtc': '6/25/2020 3:47:30 PM', 'SystemProperties': {}, 'Properties': {}, 'Body': b'{"location": {"type": "Point", "coordinates": [-75.485005, 35.474875]}, "postal_cd": "27972", "country_cd": "US", "city_name": "Salvo", "state_abbrv": "NC", "latitude": 35.474875, "longitude": -75.485005, "pk": "27972", "seq": 1, "timestamp": "2020-06-25 15:47:30", "epoch": 1593100050, "sender": "python_ms_sdk"}'}
```

```
Displaying the schema within the Avro file
{
  "fields": [
    {
      "name": "SequenceNumber",
      "type": "long"
    },
    {
      "name": "Offset",
      "type": "string"
    },
    {
      "name": "EnqueuedTimeUtc",
      "type": "string"
    },
    {
      "name": "SystemProperties",
      "type": {
        "type": "map",
        "values": [
          "long",
          "double",
          "string",
          "bytes"
        ]
      }
    },
    {
      "name": "Properties",
      "type": {
        "type": "map",
        "values": [
          "long",
          "double",
          "string",
          "bytes",
          "null"
        ]
      }
    },
    {
      "name": "Body",
      "type": [
        "null",
        "bytes"
      ]
    }
  ],
  "name": "EventData",
  "namespace": "Microsoft.ServiceBus.Messaging",
  "type": "record"
}
```

### Consume the Event Hub Stream with Azure Databricks

https://docs.microsoft.com/en-us/azure/azure-databricks/databricks-stream-from-eventhubs

