#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure Event Hubs account.
# Chris Joakim, Microsoft, 2020/06/12
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
# See https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-quickstart-cli

# az login

source ./env.sh $2

arg_count=$#
processed=0

delete() {
    processed=1
    echo 'deleting EventHubs rg: '$eventhubs_rg
    az group delete \
        --name $eventhubs_rg \
        --subscription $subscription \
        --yes \
        > out/eventhubs_rg_delete.json
}

create() {
    processed=1
    echo 'creating EventHubs rg: '$eventhubs_rg
    az group create \
        --location $eventhubs_region \
        --name $eventhubs_rg \
        --subscription $subscription \
        > out/eventhubs_rg_create.json

    echo 'creating EventHubs namespace: '$eventhubs_namespace
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

    echo 'creating EventHubs eventhub: '$eventhubs_hubname
    az eventhubs eventhub create \
        --name $eventhubs_hubname \
        --resource-group $eventhubs_rg \
        --namespace-name $eventhubs_namespace \
        --enable-capture false \
        --message-retention $eventhubs_hub_message_retention \
        --partition-count $eventhubs_hub_partition_count \
        --status $eventhubs_hub_status \
        > out/eventhubs_eventhub_create.json
}

recreate() {
    processed=1
    delete
    create
    info 
}

info() {
    processed=1
    echo 'EventHubs namespace show: '$eventhubs_namespace
    az eventhubs namespace show  \
        --name $eventhubs_namespace \
        --resource-group $eventhubs_rg \
        --subscription $subscription \
        > out/eventhubs_namespace_show.json

    echo 'EventHubs eventhub show: '$eventhubs_hubname
    az eventhubs eventhub show \
        --name $eventhubs_hubname \
        --resource-group $eventhubs_rg \
        --namespace-name $eventhubs_namespace \
        --subscription $subscription \
        > out/eventhubs_eventhub_show.json

    echo 'EventHubs authorization-rule show: '$eventhubs_keyname
    az eventhubs namespace authorization-rule show \
        --resource-group $eventhubs_rg \
        --namespace-name $eventhubs_namespace \
        --name $eventhubs_keyname \
        > out/eventhubs_auth_rule_show.json

    echo 'EventHubs authorization-rule keys list: '$eventhubs_keyname
    az eventhubs namespace authorization-rule keys list \
        --resource-group $eventhubs_rg \
        --namespace-name $eventhubs_namespace \
        --name $eventhubs_keyname \
        > out/eventhubs_auth_rule_keys_list.json
}

display_usage() {
    echo 'Usage:'
    echo './eventhubs.sh delete'
    echo './eventhubs.sh create'
    echo './eventhubs.sh recreate'
    echo './eventhubs.sh info'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "delete" ];   then delete; fi 
        if [ $arg == "create" ];   then create; fi 
        if [ $arg == "recreate" ]; then recreate; fi 
        if [ $arg == "info" ];     then info; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
