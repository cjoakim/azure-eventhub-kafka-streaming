
# =============================================================================
# Copyright (c) Microsoft Corporation. All rights reserved.
# Copyright 2016 Confluent Inc.
# Licensed under the MIT License.
# Licensed under the Apache License, Version 2.0
# Original Confluent sample modified for use with Azure Event Hubs for
# Apache Kafka Ecosystems
# =============================================================================

# This is a modified version of the source code at: 
# https://github.com/Azure/azure-event-hubs-for-kafka/tree/master/quickstart/python
#
# Python EventHub message sending client using the Confluent Kafka SDK
# (confluent-kafka @ PyPI) and not the Microsoft SDK.
# Chris Joakim, Microsoft, 2020/06/25
# Usage:
# $ python eventhub_kafka.py <send-flag-int> <max-messages-int>
# $ python eventhub_kafka.py 0 10      <-- just generate and display but not send 10 messages
# $ python eventhub_kafka.py 1 100     <-- generate send 100 messages to the Kafka EventHub

import arrow
import json
import os
import random
import sys
import time
import traceback

from confluent_kafka import Producer

def read_nc_zipcodes_data():
    return read_json('data/nc_zipcodes.json')

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def random_zipcode(zipcodes_array):
    idx = random.randint(0, len(zipcodes_array) - 1)
    zipcode = zipcodes[idx]
    utc = arrow.utcnow()
    zipcode['pk']  = zipcode['postal_cd']
    zipcode['seq'] = send_messages
    zipcode['timestamp'] = utc.format('YYYY-MM-DD HH:mm:s')
    zipcode['epoch'] = utc.timestamp
    zipcode['sender'] = 'python_kafka_sdk'
    return zipcode

def pause(message, seconds):
    print(message)
    time.sleep(seconds)


if __name__ == '__main__':
    send_messages = int(sys.argv[1])
    max_messages  = int(sys.argv[2])
    msg_count     = 0
    eh_conn_str   = os.environ['AZURE_STREAMPOC_EVENTHUB_CONN_STRING']
    eh_namespace  = os.environ['AZURE_STREAMPOC_EVENTHUB_NAMESPACE'] 
    eh_topic      = os.environ['AZURE_STREAMPOC_EVENTHUB_HUBNAME']
    eh_server     = '{}.servicebus.windows.net:9093'.format(eh_namespace)
    zipcodes      = read_nc_zipcodes_data()

    print('send_messages:      {}'.format(send_messages))
    print('max_messages:       {}'.format(max_messages))
    print('eventhub namespace: {}'.format(eh_namespace))
    print('eventhub server:    {}'.format(eh_server))
    print('eventhub topic:     {}'.format(eh_topic))
    print('eventhub conn_str:  {}'.format(eh_conn_str))
    print('# zipcodes loaded:  {}'.format(len(zipcodes)))

    conf = {
        'bootstrap.servers': eh_server, 
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': '$ConnectionString',
        'sasl.password': eh_conn_str,
        'client.id': 'python-producer'
    }
    print(json.dumps(conf, sort_keys=True, indent=2))

    pause('pausing 3 seconds after program init', 3)

    if send_messages > 0:
        print('creating kafka producer')
        p = Producer(**conf)
        print(p)
        print(str(type(p)))

        def delivery_callback(err, msg):
            if err:
                sys.stderr.write("Message failed delivery: {}\n".format(err))
            else:
                sys.stderr.write("Message delivered to; topic: {}, partition: {}, offset: {}\n".format(
                    msg.topic(), msg.partition(), msg.offset()))

        while msg_count < max_messages:
            try:
                msg_count = msg_count + 1
                zipcode = random_zipcode(zipcodes)
                msg = json.dumps(zipcode)
                print("\nsending message: {}".format(msg))
                p.produce(eh_topic, msg, callback=delivery_callback)
                p.poll(0)
                time.sleep(1)
            except:
                sys.stderr.write('Exception encountered')
                traceback.print_exc(file=sys.stderr)

        pause('pausing 10 seconds before flushing messages & exiting', 10)
        p.flush()
        print('exiting')
    else: 
        while msg_count < max_messages:
            msg_count = msg_count + 1
            zipcode = random_zipcode(zipcodes)
            msg = json.dumps(zipcode)
            print(msg)
        print('end-of-job no-send path')
