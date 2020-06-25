
# Python EventHub message sending client using the Microsoft SDK
# (azure-eventhub @ PyPI) and not Kafka.
# Chris Joakim, Microsoft, 2020/06/25
# Usage:
# $ python eventhub_sdk.py <send-flag-int> <max-messages-int>
# $ python eventhub_sdk.py 0 10      <-- just generate and display but not send 10 messages
# $ python eventhub_sdk.py 1 100     <-- generate send 100 messages to the Kafka EventHub

import arrow
import json
import os
import random
import sys
import time
import traceback

from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub import EventHubConsumerClient

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
    zipcode['sender'] = 'python_ms_sdk'
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
    eh_hubname    = os.environ['AZURE_STREAMPOC_EVENTHUB_HUBNAME']
    zipcodes      = read_nc_zipcodes_data()

    print('send_messages:      {}'.format(send_messages))
    print('max_messages:       {}'.format(max_messages))
    print('eventhub namespace: {}'.format(eh_namespace))
    print('eventhub hubname:   {}'.format(eh_hubname))
    print('eventhub conn_str:  {}'.format(eh_conn_str))
    print('# zipcodes loaded:  {}'.format(len(zipcodes)))

    if send_messages > 0:
        print('creating EventHubProducerClient')
        eh_client = EventHubProducerClient.from_connection_string(
            eh_conn_str, eventhub_name=eh_hubname)

        while msg_count < max_messages:
            try:
                msg_count = msg_count + 1
                msg = json.dumps(random_zipcode(zipcodes))
                batch_of_1 = eh_client.create_batch()
                batch_of_1.add(EventData(msg))
                print("\nsending message: {}".format(msg))
                eh_client.send_batch(batch_of_1)
                time.sleep(1)
            except:
                sys.stderr.write('Exception encountered')
                traceback.print_exc(file=sys.stderr)

        if eh_client:
            eh_client.close()
        pause('pausing 10 seconds before flushing messages & exiting', 10)
        print('exiting')
    else: 
        while msg_count < max_messages:
            msg_count = msg_count + 1
            zipcode = random_zipcode(zipcodes)
            msg = json.dumps(zipcode)
            print(msg)
        print('end-of-job no-send path')
