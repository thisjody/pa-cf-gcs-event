# PA-CF-GCS-EVENT Cloud Function

The `pa-cf-gcs-event` is a Google Cloud Function designed to detect specific `.csv` file patterns stored in Google Cloud Storage and subsequently publish an event message to Pub/Sub.

## Functionality Overview

The `gcs_event_to_pubsub` function operates as follows:

1. Logs the event type and timestamp from the triggering GCS event.
2. Checks if the uploaded resource's name matches a specific `.csv` pattern.
3. If matched, constructs a message containing the type, bucket name, and file name.
4. Publishes the message to a specified Pub/Sub topic.

## Error Handling

- Publishing errors: Logged and halt the function.
- Non-matching resources: Generate corresponding log entries.

## Dependencies

The Cloud Function leverages the Python packages defined in the `requirements.txt`:

- `google-cloud-pubsub`
- `google-cloud-storage`
- `google-auth-httplib2`
- `google-auth-oauthlib`
- `google-cloud-secret-manager`
- `google-auth`

## Roles and Service Accounts

Two custom roles are utilized:

1. Deploy Role (custom_role_pa_cf_deploy):

- Role for deploying the Cloud Function.
- Definition: `pa-cf-deploy-role.json`.

2. Privileged Role (custom_role_pa_gcs_ps_privileged):

- Privileged role for the Cloud Function to publish messages to Pub/Sub, read from GCS, and more.
- Definition: `pa-gcs-ps-privileged-role.json`.

## Service Accounts

Two service accounts are employed:

1. **Deploy Service Account (`pa-cf-deploy-sa`)**: Used for deploying the function.
2. **Privileged Service Account (`pa-gcs-ps-privileged-sa`)**: Used for higher-level operations like publishing messages.

## Impersonation

The function uses service account impersonation for elevated tasks. This means the deploying service account (pa-cf-deploy-sa) impersonates the privileged service account (pa-gcs-ps-privileged-sa) when specific privileges are required.


### Role and Service Account Automation

A shell script, `create_role_and_sa_bind.sh`, has been provided to automate the processes of:

1. Checking, creating, or updating the custom role.
2. Creating service accounts if they don't exist.
3. Granting Service Account Token Creator role to the deploy service account for impersonation.
4. Binding the custom role to the service account.
5. Managing secrets in Google Secret Manager.

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

```
./pa_deploy.sh
```

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
  - A script, `create_role_and_sa_bind.sh`, is provided to manage the creation of the custom role and service account. It's essential to run this before deploying the function to ensure proper IAM configurations.

- **Deployment**: 
  - Use the `gcloud` command-line tool with configurations in the `pa_edeploy.sh` script.

