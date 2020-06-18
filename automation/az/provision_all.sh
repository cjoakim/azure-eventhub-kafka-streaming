#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of 
# all Azure resources in this POC.
# Chris Joakim, Microsoft, 2020/06/18

# az login

echo 'extensions'
./extensions.sh install

echo '=== eventhubs'
./eventhubs.sh recreate

echo '=== storage'
./storage.sh create

echo '=== adl'
./adl.sh create

echo '=== cosmos_sql'
./cosmos_sql.sh create

echo '=== stream_analytics'
./stream_analytics.sh create

echo '=== done'
