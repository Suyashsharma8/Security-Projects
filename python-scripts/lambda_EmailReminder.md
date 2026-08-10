

'''python
import json
import boto3
import os

sns = boto3.client("sns")
ec2 = boto3.client("ec2")

TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event, indent=2))

    instance_id = event["instance_id"]

    response = ec2.describe_instances(
        InstanceIds=[instance_id]
    )

    instance = response["Reservations"][0]["Instances"][0]

    state = instance["State"]["Name"]

    print(f"Instance {instance_id} is {state}")

    if state == "running":

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="EC2 Reminder",
            Message=f"""Your EC2 instance is still running.

Instance ID:
{instance_id}

Current state:
{state}

Consider stopping it if you no longer need it.
"""
        )

        print("Reminder email sent.")

    else:

        print("Instance already stopped. No email sent.")

    return {
        "statusCode": 200,
        "instance_state": state
    }
