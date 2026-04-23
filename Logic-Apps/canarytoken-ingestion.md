This logic-app can parse the incoming webhook, we need to add an action for it to send the data into Azure Sentinel. This requires the Log Analytics Data Collector connector and the Send Data action.

```json
{
    "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "contentVersion": "1.0.0.0",
        "triggers": {
            "When_an_HTTP_request_is_received": {
                "type": "Request",
                "kind": "Http",
                "inputs": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "Description": {
                                "type": "string"
                            },
                            "Triggered": {
                                "type": "integer"
                            },
                            "Timestamp": {
                                "type": "string"
                            },
                            "Token": {
                                "type": "string"
                            },
                            "Intro": {
                                "type": "string"
                            },
                            "Reminder": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        "actions": {
            "Send_Data": {
                "runAfter": {},
                "type": "ApiConnection",
                "inputs": {
                    "host": {
                        "connection": {
                            "name": "@parameters('$connections')['azureloganalyticsdatacollector']['connectionId']"
                        }
                    },
                    "method": "post",
                    "body": "@{triggerBody()}",
                    "headers": {
                        "Log-Type": "canarytokens"
                    },
                    "path": "/api/logs"
                }
            }
        },
        "outputs": {},
        "parameters": {
            "$connections": {
                "type": "Object",
                "defaultValue": {}
            }
        }
    },
    "parameters": {
        "$connections": {
            "type": "Object",
            "value": {
                "azureloganalyticsdatacollector": {
                    "id": "/subscriptions/**************/providers/Microsoft.Web/locations/westeurope/managedApis/azureloganalyticsdatacollector",
                    "connectionId": "/subscriptions/******************/resourceGroups/************/providers/Microsoft.Web/connections/azureloganalyticsdatacollector-2",
                    "connectionName": "azureloganalyticsdatacollector-2",
                    "connectionProperties": {}
                }
            }
        }
    }
}
