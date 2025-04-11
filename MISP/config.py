#This script can be used to upload and export indicators to sentinel
# Code for supporting storage of secrets in key vault (only works for VMs running on Azure)
#import os
#from azure.keyvault.secrets import SecretClient
#from azure.identity import DefaultAzureCredential

# Key vault section
# Key Vault name must be a globally unique DNS name
#keyVaultName = "<unique-name>"
#KVUri = f"https://{keyVaultName}.vault.azure.net"

# Log in with the virtual machines managed identity
#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=KVUri, credential=credential)

# Retrieve values from KV (client secret, MISP-key most importantly)
#retrieved_mispkey = client.get_secret('MISP-Key')
#retrieved_clientsecret = client.get_secret('ClientSecret')

# Set values with 
# misp_key = retrieved_mispkey.value
# 'client_secret': retrieved_clientsecret.value

Microsoft section
ms_auth = {
    'tenant':'xxxxxxxxxxxxxxx',
    'client_id':'xxxxxxxxxxxxxxx',
    'client_secret':'xxxxxxxxxxxxxxx',
    'graph_api':False,                                 # Set to False to use Upload Indicators API   
    #'scope': 'https://graph.microsoft.com/.default',   # Scope for GraphAPI
    'scope':'https://management.azure.com/.default',   # Scope for Upload Indicators API
    'workspace_id':'xxxxxxxxxxxxxxx'
}

ms_passiveonly = False              # Graph API only
ms_action = 'alert'                 # Graph API only

ms_api_version = "2022-07-01"       # Upload Indicators API version
ms_max_indicators_request = 100     # Upload Indicators API: Throttle max: 100 indicators per request
ms_max_requests_minute = 100        # Upload Indicators API: Throttle max: 100 requests per minute


####
# MISP section
misp_key = 'xxxxxxxxxxxxxxxxxxxx'
misp_domain = '<enter your domain>'
misp_verifycert = False
timeout = 120

misp_event_filters = {
    "published": 1,
    "tags": [ " you can add customs tags" ],
    #"enforceWarninglist": True,
    "includeEventTags": True,
    "publish_timestamp": "14d",
}

misp_event_limit_per_page = 512     # Upload Indicators API: Limit memory use when querying MISP for STIX packages

####
# Integration settings

ignore_localtags = True
network_ignore_direction = True     # Graph API only

default_confidence = 85             # Sentinel default confidence level of indicator

days_to_expire = 60                 # Graph API and Upload Indicators
days_to_expire_start = "current_date" # Upload Indicators API only. Start counting from "valid_from" | "current_date" ; 
days_to_expire_mapping = {          # Upload indicators API only. Mapping for expiration of specific indicator types
                    "ipv4-addr": 180,
                    "ipv6-addr": 180,
                    "domain-name": 180,
                    "url": 180,
                }
                                    # Don't set an expiration date for files ('file')

log_file = "/var/log/misp2sentinel.log"
write_post_json = False             # Graph API only
verbose_log = False
write_parsed_indicators = True     # Upload Indicators only
write_parsed_eventid = True

misp_flatten_attributes = True      # Convert all attributes in objects to "atomic" attributes. This can help when attributes are not "mapped" in misp-stix
