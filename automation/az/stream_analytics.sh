#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure Stream Analytics account.
# Chris Joakim, Microsoft, 2020/06/12

# az login

source ./env.sh $2

arg_count=$#
processed=0

create() {
    processed=1
    echo 'creating stream_analytics rg: '$stream_analytics_rg
    az group create \
        --location $stream_analytics_region \
        --name $stream_analytics_rg \
        --subscription $subscription \
        > out/stream_analytics_rg_create.json

    echo 'creating stream_analytics acct: '$stream_analytics_name
    az stream-analytics job create \
        --name $stream_analytics_name \
        --resource-group $stream_analytics_rg \
        --location $stream_analytics_region \
        > out/stream_analytics_acct_create.json
}

display_usage() {
    echo 'Usage:'
    echo './stream_analytics.sh create'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "create" ]; then create; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
