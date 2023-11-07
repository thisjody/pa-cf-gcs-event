from google.cloud import pubsub_v1, secretmanager
import logging
from google.oauth2 import service_account
from google.auth.transport import requests
from google.auth import impersonated_credentials
import os
import json
import re

logging.basicConfig(level=logging.INFO)

# Setup the auth and request for token
auth_request = requests.Request()
PROJECT_ID = os.getenv('PROJECT_ID')

IMPERSONATE_SA_MAP = {
    'publish': os.environ['PUBLISH_SA']
}

def get_secret(secret_name):
    """Retrieve secrets from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('UTF-8'))

def extract_info(resource_name):
    """Check if the resource name matches the desired pattern and extract dataset and table names."""
    csv_pattern = os.getenv('CSV_PATTERN_REGEX')
    if not csv_pattern:
        raise ValueError("CSV_PATTERN_REGEX environment variable not set.")
    
    match = re.match(csv_pattern, resource_name)
    if match:
        dataset_name = f"{match.group(1)}_{match.group(2)}"
        table_name = match.group(3).replace('-', '_')
        return dataset_name.lower(), table_name.lower()
    else:
        return None, None

def get_impersonated_credentials(action='publish'):
    """Retrieve impersonated credentials."""
    sa_credentials_secret_name = os.getenv('SA_CREDENTIALS_SECRET_NAME')
    sa_credentials = get_secret(sa_credentials_secret_name)
    credentials = service_account.Credentials.from_service_account_info(sa_credentials)
    target_principal = IMPERSONATE_SA_MAP.get(action)
    if not target_principal:
        raise ValueError(f"No service account mapped for action: {action}")
    target_scopes = os.getenv('TARGET_SCOPES').split(",")
    return impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=target_principal,
        target_scopes=target_scopes,
        lifetime=600
    )

def publish_to_topic(message_data):
    """Publish the given message data to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient(credentials=get_impersonated_credentials())
    topic_path = publisher.topic_path(PROJECT_ID, os.getenv('PUBLISH_TOPIC_NAME'))
    return publisher.publish(topic_path, message_data)

def gcs_event_to_pubsub(data, context):
    """Function to handle GCS events and publish relevant ones to a Pub/Sub topic."""
    logging.info(f"Event type: {context.event_type}")
    logging.info(f"Event timestamp: {context.timestamp}")

    resource_name = data['name'].rstrip('/')
    
    dataset_name, table_name = extract_info(resource_name)
    if dataset_name and table_name:
        message = {
            "type": "csv",
            "bucket": data["bucket"],
            "file_name": resource_name,
            "dataset_name": dataset_name,
            "table_name": table_name  # Include the extracted table name here
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
