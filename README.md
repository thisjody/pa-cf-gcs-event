# PA-CF-GCS-EVENT Cloud Function

## Overview
This cloud function, named `gcs_event_to_pubsub`, is designed to handle events from Google Cloud Storage (GCS). When specific GCS events occur, particularly concerning files with a certain naming pattern, this function triggers and publishes relevant information to a Google Pub/Sub topic.

The function operates as follows:

1. It listens to events from GCS.
2. Extracts the resource name from the incoming event.
3. Checks if the resource name (in this case, the file name) matches a desired pattern, which is primarily CSV files with a specific naming convention.
4. If the file name matches the pattern, it formats a message and publishes it to a Pub/Sub topic. If not, it logs that the resource failed the regex match.
5. For secure authentication and authorization purposes, the function utilizes impersonated credentials.

## Prerequisites
Before deploying and using this cloud function, ensure you have:

- **Google Cloud SDK**: Ensure the Google Cloud SDK is installed, as it provides tools to interact with Google Cloud resources. [Official Documentation](https://cloud.google.com/sdk/docs/install).
  
- **Google Cloud Project**: This function requires a Google Cloud Project where the Cloud Function, GCS, and Pub/Sub reside. Have the `PROJECT_ID` at hand.
  
- **Environment Variables**: The function utilizes several environment variables, such as:
    - `PROJECT_ID`: Your Google Cloud Project's ID.
    - `SA_CREDENTIALS_SECRET_NAME`: Secret name containing the service account credentials.
    - `IMPERSONATE_SA`: Service account to impersonate.
    - `TARGET_SCOPES`: Required scopes for the impersonated service account.
    - `TOPIC_NAME`: Name of the Pub/Sub topic for message publishing.

- **Google Secret Manager**: Store necessary secrets, like service account credentials.

- **Google Cloud Storage (GCS)**: This function reacts to GCS bucket events. Ensure a GCS bucket is set up and capable of generating events.

- **Google Pub/Sub**: Create a Pub/Sub topic for the function to publish messages. Set up the necessary permissions for publishing.

- **Permissions**: The function and its service account should have permissions for accessing Secret Manager, impersonating other service accounts, and publishing messages to Pub/Sub.

## Functionality Overview
1. Logs the event type and timestamp from the triggering GCS event.
2. Checks if the uploaded resource's name matches a specific `.csv` pattern.
3. If matched, constructs a message containing the type, bucket name, and file name.
4. Publishes the message to a specified Pub/Sub topic.

## Error Handling
- Publishing errors are logged and halt the function.
- Non-matching resources generate log entries.

## Dependencies
The Cloud Function utilizes Python packages from `requirements.txt`:

- `google-cloud-pubsub`
- `google-cloud-storage`
- `google-auth-httplib2`
- `google-auth-oauthlib`
- `google-cloud-secret-manager`
- `google-auth`

## Roles and Service Accounts
- **Deploy Role (`custom_role_pa_cf_deploy`)**:
   - For deploying the Cloud Function.
   - Definition: `pa-cf-deploy-role.json`.
   
- **Privileged Role (`custom_role_pa_gcs_ps_privileged`)**:
   - For tasks like message publishing to Pub/Sub, GCS reading, etc.
   - Definition: `pa-gcs-ps-privileged-role.json`.

## Service Accounts
- **Deploy Service Account (`pa-cf-deploy-sa`)**: For deployment.
- **Privileged Service Account (`pa-gcs-ps-privileged-sa`)**: For elevated operations.

## Impersonation
The function uses service account impersonation. The deploying service account (`pa-cf-deploy-sa`) impersonates the privileged service account (`pa-gcs-ps-privileged-sa`) for certain tasks.

## Deployment Script for PA-CF-GCS-EVENT Cloud Function

The `pa_deploy.sh` script simplifies the deployment of the pa-cf-gcs-event Cloud Function by automating the process, ensuring the necessary prerequisites are met, and setting up the correct environment variables for deployment.

## Usage
To use the script:
 
```
./pa_deploy.sh
```

 This script wraps the following `gcloud` command:


