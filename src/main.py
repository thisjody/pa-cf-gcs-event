from google.cloud import pubsub_v1, secretmanager
from google.oauth2 import service_account
from google.auth.transport import requests
from google.auth import impersonated_credentials
import os
import json
import re

# Setup the auth and request for token
auth_request = requests.Request()

PROJECT_ID = os.getenv('PROJECT_ID')

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('UTF-8'))

# Obtain service account credentials from Secret Manager
sa_credentials = get_secret('pa-cf-deploy-sa-credentials')

# Load the credentials for the less privileged SA from the secret
credentials = service_account.Credentials.from_service_account_info(sa_credentials)

target_principal = os.getenv('IMPERSONATE_SA')
target_scopes = os.getenv('TARGET_SCOPES').split(",")

# Build impersonated credentials for the target service account
impersonated_creds = impersonated_credentials.Credentials(
    source_credentials=credentials,
    target_principal=target_principal,
    target_scopes=target_scopes,
    lifetime=600  # in seconds, optional
)

# Create a Pub/Sub publisher client using impersonated credentials
publisher = pubsub_v1.PublisherClient(credentials=impersonated_creds)
topic_path = publisher.topic_path(PROJECT_ID, os.getenv('TOPIC_NAME'))

def gcs_event_to_pubsub(data, context):
    print(f"Event type: {context.event_type}")
    print(f"Event timestamp: {context.timestamp}")

    resource_name = data['name'].rstrip('/')

    csv_pattern = r'(?i)^\d{4}/\d{2}/uaf-acep-[\w-]+/uaf-acep-[\w-]+_\d{4}-\d{2}-\d{2}\.csv$'

    if re.match(csv_pattern, resource_name):
        # The resource is a .csv file
        message = {
            "type": "csv",
            "bucket": data["bucket"],
            "file_name": resource_name
        }
        message_data = json.dumps(message).encode('utf-8')
        
        try:
            publish_message = publisher.publish(topic_path, message_data)
            publish_message.result()
        except Exception as e:
            print(f'An error occurred when trying to publish message: {str(e)}')
            raise
        else:
            print(f"Published message for resource {resource_name} in bucket {data['bucket']}")

    else:
        print(f"Failed regex match for resource: {resource_name}")
