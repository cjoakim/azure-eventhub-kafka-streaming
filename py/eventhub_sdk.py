"""
Python EventHub client using the Microsoft SDK (azure-eventhub @ PyPI) and not Kafka.

Usage:
  python eventhub_sdk.py producer <send-flag-int> <max-events-int> <optional-sleep-seconds>
  python eventhub_sdk.py producer 0 10
  python eventhub_sdk.py producer 1 100 0.1
  -
  python eventhub_sdk.py consumer <group> <starting_position> <count>
  python eventhub_sdk.py consumer $Default -1 10
  python eventhub_sdk.py consumer groupa -1 10
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Links:
# https://docs.microsoft.com/en-us/python/api/azure-eventhub/azure.eventhub.aio.eventhubconsumerclient?view=azure-python
# https://docs.microsoft.com/en-us/python/api/overview/azure/eventhub-readme?view=azure-python#consume-events-from-an-event-hub

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "2020.07.13"

import arrow
import json
import os
import random
import sys
import time
import traceback

from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub import EventHubConsumerClient

from docopt import docopt

# global variables
consumer_group = None
max_events_to_receive = 0
events_received_count = 0
client = None
sleep_seconds = 1.0


def send_events(do_send, max_events):
    event_count   = 0
    eh_conn_str   = os.environ['AZURE_STREAMPOC_EVENTHUB_CONN_STRING']
    eh_namespace  = os.environ['AZURE_STREAMPOC_EVENTHUB_NAMESPACE'] 
    eh_hubname    = os.environ['AZURE_STREAMPOC_EVENTHUB_HUBNAME']
    zipcodes      = read_nc_zipcodes_data()
    start_epoch   = arrow.utcnow().timestamp

    print('send_events')
    print('do_send:            {}'.format(do_send))
    print('max_events:         {}'.format(max_events))
    print('sleep_seconds:      {}'.format(sleep_seconds))
    print('eventhub namespace: {}'.format(eh_namespace))
    print('eventhub hubname:   {}'.format(eh_hubname))
    print('eventhub conn_str:  {}'.format(eh_conn_str))
    print('# zipcodes loaded:  {}'.format(len(zipcodes)))

    if do_send > 0:
        print('creating EventHubProducerClient')
        client = EventHubProducerClient.from_connection_string(
            eh_conn_str, eventhub_name=eh_hubname)

        while event_count < max_events:
            try:
                event_count = event_count + 1
                evt = json.dumps(random_zipcode(zipcodes))
                batch_of_1 = client.create_batch()
                batch_of_1.add(EventData(evt))
                print("\nsending event: {}".format(evt))
                client.send_batch(batch_of_1)
                time.sleep(sleep_seconds)
            except:
                sys.stderr.write('Exception encountered')
                traceback.print_exc(file=sys.stderr)

        if client:
            client.close()
            time.sleep(2)

        print("query cosmosdb with: SELECT * FROM c where c.sender = '{}' and c.epoch >= {}".format(
            'python_ms_sdk', start_epoch))
    else: 
        while event_count < max_events:
            event_count = event_count + 1
            zipcode = random_zipcode(zipcodes)
            evt = json.dumps(zipcode, sort_keys=False, indent=2)
            print(evt)
        print('end-of-job producer no-send path')

def consume_events(starting_position):
    global consumer_group
    global events_received_count
    global max_events_to_receive
    global client
    event_count  = 0
    eh_conn_str  = os.environ['AZURE_STREAMPOC_EVENTHUB_CONN_STRING']
    eh_namespace = os.environ['AZURE_STREAMPOC_EVENTHUB_NAMESPACE'] 
    eh_hubname   = os.environ['AZURE_STREAMPOC_EVENTHUB_HUBNAME']
    zipcodes     = read_nc_zipcodes_data()
    start_epoch  = arrow.utcnow().timestamp
    consumer_group = reformat_consumer_group(consumer_group)

    print('consume_events')
    print('consumer_group:        {}'.format(consumer_group))
    print('starting_position:     {}'.format(starting_position))
    print('max_events_to_receive: {}'.format(max_events_to_receive))
    print('eventhub namespace:    {}'.format(eh_namespace))
    print('eventhub hubname:      {}'.format(eh_hubname))
    print('eventhub conn_str:     {}'.format(eh_conn_str))
    event_count = 0

    if max_events_to_receive > 0:
        print('creating EventHubConsumerClient')
        client = EventHubConsumerClient.from_connection_string(
            eh_conn_str, consumer_group, eventhub_name=eh_hubname)

        # "-1" is from the beginning of the partition.
        client.receive(on_event=on_event_received, starting_position=starting_position)  

def on_event_received(partition_context, event):
    global consumer_group
    global events_received_count
    global max_events_to_receive
    global client
    events_received_count = events_received_count + 1

    print("Received event; group: {} partition: {}\nevent: {}".format(
        consumer_group, partition_context.partition_id, event))
    partition_context.update_checkpoint(event)
    if events_received_count >= max_events_to_receive:
        print('max events received: {}.  closing client and exiting...'.format(max_events_to_receive))
        client.close()
        sys.exit()

def reformat_consumer_group(s):
    if s.lower() == 'default':
        return '$Default'
    else:
        return s

def read_nc_zipcodes_data():
    return read_json('data/nc_zipcodes.json')

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def random_zipcode(zipcodes_array):
    idx = random.randint(0, len(zipcodes_array) - 1)
    zipcode = zipcodes_array[idx]
    utc = arrow.utcnow()
    zipcode['pk']  = zipcode['postal_cd']
    zipcode['idx'] = idx
    zipcode['timestamp'] = utc.format('YYYY-MM-DD HH:mm:s')
    zipcode['epoch'] = utc.timestamp
    zipcode['sender'] = 'python_ms_sdk'
    return zipcode

def pause(message, seconds):
    print(message)
    time.sleep(seconds)

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == '__main__':
    print(sys.argv)
    
    if len(sys.argv) > 1:
        client_type = sys.argv[1]

        if client_type == 'producer':
            do_send = int(sys.argv[2])
            max_events = int(sys.argv[3])
            if len(sys.argv) > 4:
                sleep_seconds = float(sys.argv[4])
            send_events(do_send, max_events)

        elif client_type == 'consumer':
            consumer_group = sys.argv[2]
            starting_position = int(sys.argv[3])
            max_events_to_receive = int(sys.argv[4])
            consume_events(starting_position)

        else:
            print_options('Error: invalid arg {}'.format(client_type))
    else:
        print_options('Error: no command-line args')
