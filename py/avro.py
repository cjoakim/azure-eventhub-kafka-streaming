
# See https://www.perfectlyrandom.org/2019/11/29/handling-avro-files-in-python/
# Chris Joakim, Microsoft, 2020/06/12

import copy
import json

import os
import random
import sys
import time
import traceback

import avro
import fastavro


if __name__ == '__main__':
    infile = sys.argv[1]
    print('infile: {}'.format(infile))

    with open(infile, 'rb') as f:
        print('Displaying the messages in Avro file: {}'.format(infile))
        reader = fastavro.reader(f)
        for eh_message in reader:
            print('')
            print(eh_message)

        print('')
        print('Displaying the schema within the Avro file')
        metadata = copy.deepcopy(reader.metadata)
        schema_from_file = json.loads(metadata['avro.schema'])
        print(json.dumps(schema_from_file, sort_keys=True, indent=2))
