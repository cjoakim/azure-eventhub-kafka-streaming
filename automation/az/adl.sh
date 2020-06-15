#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure DataLake Gen2 account (a storage account, really).
# Chris Joakim, Microsoft, 2020/06/12
#
# https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-directory-file-acl-cli
#
# az extension add -n storage-preview  ?

# az login

source ./env.sh $2

arg_count=$#
processed=0

delete() {
    processed=1
    echo 'deleting adl_gen2 rg: '$adl_rg
    az group delete \
        --name $adl_rg \
        --subscription $subscription \
        --yes \
        > out/adl_rg_delete.json
}

create() {
    processed=1
    echo 'creating adl_gen2 rg: '$adl_rg
    az group create \
        --location $adl_region \
        --name $adl_rg \
        --subscription $subscription \
        > out/adl_rg_create.json

    echo 'creating adl gen2 acct: '$adl_name
    az storage account create \
        --name $adl_name \
        --resource-group $adl_rg \
        --location $adl_region \
        --sku $adl_sku \
        --kind StorageV2 \
        --hierarchical-namespace true \
        > out/adl_acct_create.json

    # note: kind 'StorageV2' and '--hierarchical-namespace true'
    # makes it a Data Lake Gen2
}

recreate() {
    processed=1
    delete
    create
    info 
}

info() {
    processed=1
    echo 'storage acct show: '$adl_name
    az storage account show \
        --name $adl_name \
        --resource-group $adl_rg \
        --subscription $subscription \
        > out/adl_acct_show.json

    echo 'storage acct keys: '$adl_name
    az storage account keys list \
        --account-name $adl_name \
        --resource-group $adl_rg \
        --subscription $subscription \
        > out/adl_acct_keys.json
}

display_usage() {
    echo 'Usage:'
    echo './adl.sh delete'
    echo './adl.sh create'
    echo './adl.sh recreate'
    echo './adl.sh info'
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
