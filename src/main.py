from google.cloud import pubsub_v1
import os
import json
import re

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('PROJECT_ID'), os.getenv('TOPIC_NAME'))

def gcs_event_to_pubsub(data, context):
    print(f"Event type: {context.event_type}")
    print(f"Event timestamp: {context.timestamp}")

    resource_name = data['name'].rstrip('/')

    #csv_pattern = r'^\d{4}/\d{2}/uaf-acep-[\w-]+/uaf-acep-[\w-]+_\d{4}-\d{2}-\d{2}\.csv$'
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