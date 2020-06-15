#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure Storage account.
# Chris Joakim, Microsoft, 2020/06/12

# az login

source ./env.sh $2

arg_count=$#
processed=0

list() {
    processed=1
    echo 'listing available az cli extensions ...'
    az extension list-available --output table

    echo 'listing installed az cli extensions ...'
    az extension list --output table
}

install() {
    processed=1
    echo 'adding storage-preview extension ...'
    az extension add -n storage-preview

    echo 'adding sstream-analytics extension ...'
    az extension add -n stream-analytics
}

display_usage() {
    echo 'Usage:'
    echo './extensions.sh list'
    echo './extensions.sh install'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "list" ];    then list; fi 
        if [ $arg == "install" ]; then install; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
