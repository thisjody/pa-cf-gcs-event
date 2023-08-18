# PA-CF-GCS-EVENT Cloud Function

The `pa-cf-gcs-event` is a Google Cloud Function designed to detect specific `.csv` file patterns stored in Google Cloud Storage and subsequently publish an event message to Pub/Sub.

## Functionality Overview

The `gcs_event_to_pubsub` function operates as follows:

1. Logs the event type and timestamp from the triggering GCS event.
2. Checks if the uploaded resource's name matches a specific `.csv` pattern.
3. If matched, constructs a message containing the type, bucket name, and file name.
4. Publishes the message to a specified Pub/Sub topic.

### Exception Handling

Should there be any issues with publishing to Pub/Sub, the function will log an error message and raise an exception to halt its operation. If the uploaded resource doesn't match the `.csv` pattern, a log entry detailing the failed regex match will be generated.

## Dependencies

The Cloud Function leverages the Python packages defined in the `requirements.txt`:

- `google-cloud-pubsub`
- `google-cloud-storage`

## Custom Role and Service Account

The function employs a specific custom role, `custom_role_pa_cf_gcs_event`, granting it permissions to:

- Publish to Pub/Sub.
- Read from GCS.
- Receive events from Eventarc.
- Invoke routes using Cloud Run infrastructure.

The custom role's definition can be found in the `custom_role.json` file. This role has been crafted to strictly adhere to the principle of least privilege, ensuring that the function is only granted permissions essential for its tasks.

### Service Account Configuration

To seamlessly and securely perform its tasks, a dedicated service account named `pa-cf-gcs-event-sa` is used.

### Role and Service Account Automation

A shell script, `create_role_and_sa_bind.sh`, has been provided to automate the processes of:

- Checking, creating, or updating the custom role.
- Checking or creating the service account.
- Binding the custom role to the service account.

**Note**: Before deploying the Cloud Function using `pa_deploy.sh`, ensure that the custom role and service account are correctly created and bound. The Cloud Function deployment is dependent on these IAM configurations. Run the automation script as follows:

```bash
./create_role_and_sa_bind.sh
```

This script will:

1. Check for the existence of the custom role and service account.
2. Create or update the custom role based on the definitions in custom_role.json.
3. Create the service account if it doesn't already exist.
4. Bind the custom role to the service account to grant the necessary permissions.
Ensure this step completes successfully before proceeding with the deployment.

## Deployment

To deploy the Cloud Function, the gcloud command-line tool is used. Deployment configurations, including runtime, region, memory allocation, and environment variables, are specified in the `pa_edeploy.sh` script:

## Summary

The gcs_event_to_pubsub function operates as follows:

- **Function Purpose**: 
  - The Cloud Function `pa-cf-gcs-event` detects specific `.csv` files uploaded to Google Cloud Storage and publishes a corresponding event to Pub/Sub.
  
- **Function Flow**:
  1. Logs event details.
  2. Matches resource name to a `.csv` pattern.
  3. Constructs and publishes a message to Pub/Sub if matched.

- **Error Handling**:
  - Errors in publishing are logged and halt the function. Mismatched resources also generate log entries.

- **Dependencies**: 
  - The function depends on Python packages `google-cloud-pubsub` and `google-cloud-storage`.

- **Custom Role & Service Account**:
  - The function utilizes a custom role, `custom_role_pa_cf_gcs_event`, ensuring limited, task-specific permissions.
  - A dedicated service account, `pa-cf-gcs-event-sa`, is used for function operations.

- **Automation**:
  - A script, `create_role_and_sa_bind.sh`, is provided to manage the custom role and service account. It's essential to run this before deploying the function to ensure proper IAM configurations.

- **Deployment**: 
  - Use the `gcloud` command-line tool with configurations in the `pa_edeploy.sh` script.

