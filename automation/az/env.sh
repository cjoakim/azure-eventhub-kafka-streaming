#!/bin/bash

# Bash shell that defines parameters and environment variables used 
# in this app, and is "sourced" by the other scripts in this repo.
# Chris Joakim, Microsoft, 2020/06/12

# ===

# environment variables for provisioning:

export subscription=$AZURE_SUBSCRIPTION_ID
export user=$USER
export primary_region="eastus"
export primary_rg="cjoakim-stream-poc"
#
export adl_region=$primary_region
export adl_rg=$primary_rg
export adl_name="cjoakimstreamadl"
export adl_kind="StorageV2"       # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export adl_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export adl_access_tier="Hot"      # Cool, Hot
#
export cosmos_sql_region=$primary_region
export cosmos_sql_rg=$primary_rg
export cosmos_sql_acct_name="cjoakimstreamcdb"
export cosmos_sql_acct_consistency="Session"    # {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}
export cosmos_sql_acct_kind="GlobalDocumentDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_sql_dbname="dev"
export cosmos_sql_events_collname="events"
export cosmos_sql_events_pk="/pk"
export cosmos_sql_events_ru="1000"
#
export eventhubs_region=$primary_region
export eventhubs_rg=$primary_rg
export eventhubs_namespace="cjoakimstreameh"
export eventhubs_hubname="dev"
export eventhubs_enable_kafka="true"
export eventhubs_enable_auto_inflate="true"
export eventhubs_max_tu="3"
export eventhubs_sku="Standard"
export eventhubs_keyname="RootManageSharedAccessKey"
export eventhubs_hub_message_retention="1"
export eventhubs_hub_partition_count="1"
export eventhubs_hub_status="Active"
#
export storage_region=$primary_region
export storage_rg=$primary_rg
export storage_name="cjoakimstreamstor"
export storage_kind="BlobStorage"     # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export storage_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export storage_access_tier="Hot"      # Cool, Hot

export stream_analytics_region=$primary_region
export stream_analytics_rg=$primary_rg
export stream_analytics_name="cjoakimstreama"
