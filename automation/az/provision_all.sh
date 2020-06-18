#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of 
# all Azure resources in this POC.
# Chris Joakim, Microsoft, 2020/06/18

# az login

echo 'extensions'
./extensions.sh

echo '=== eventhubs'
./eventhubs.sh

echo '=== storage'
./storage.sh

echo '=== adl'
./adl.sh

echo '=== cosmos_sql'
./cosmos_sql.sh

echo '=== stream_analytics'
./stream_analytics.sh

echo '=== done'
