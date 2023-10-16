from google.cloud import pubsub_v1, secretmanager
import logging
from google.oauth2 import service_account
from google.auth.transport import requests
from google.auth import impersonated_credentials
import os
import json
import re

# This line is optional but will ensure that log statements of level INFO and above are shown
logging.basicConfig(level=logging.INFO)

# Setup the auth and request for token
auth_request = requests.Request()
PROJECT_ID = os.getenv('PROJECT_ID')

def get_secret(secret_name):
    """Retrieve secrets from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('UTF-8'))

def is_valid_file(resource_name):
    """Check if the resource name matches the desired pattern."""
    csv_pattern = r'(?i)^\d{4}/\d{2}/uaf-acep-[\w-]+/uaf-acep-[\w-]+_\d{4}-\d{2}-\d{2}\.csv$'
    return re.match(csv_pattern, resource_name)

def get_impersonated_credentials():
    """Retrieve impersonated credentials."""
    sa_credentials_secret_name = os.environ.get('SA_CREDENTIALS_SECRET_NAME')
    sa_credentials = get_secret(sa_credentials_secret_name)
    credentials = service_account.Credentials.from_service_account_info(sa_credentials)
    target_principal = os.getenv('IMPERSONATE_SA')
    target_scopes = os.getenv('TARGET_SCOPES').split(",")

    return impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=target_principal,
        target_scopes=target_scopes,
        lifetime=600  # in seconds, optional
    )

def publish_to_topic(message_data):
    """Publish the given message data to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient(credentials=get_impersonated_credentials())
    topic_path = publisher.topic_path(PROJECT_ID, os.getenv('TOPIC_NAME'))
    return publisher.publish(topic_path, message_data)

def gcs_event_to_pubsub(data, context):
    """Function to handle GCS events and publish relevant ones to a Pub/Sub topic."""
    logging.info(f"Event type: {context.event_type}")
    logging.info(f"Event timestamp: {context.timestamp}")

    resource_name = data['name'].rstrip('/')
    
    if is_valid_file(resource_name):
        message = {
            "type": "csv",
            "bucket": data["bucket"],
            "file_name": resource_name
        }
        message_data = json.dumps(message).encode('utf-8')

        try:
            publish_message = publish_to_topic(message_data)
            publish_message.result()
        except Exception as e:
            logging.error(f'An error occurred when trying to publish message: {str(e)}')
            raise
        else:
            logging.info(f"Published message for resource {resource_name} in bucket {data['bucket']}")
    else:
        logging.warning(f"Failed regex match for resource: {resource_name}")
