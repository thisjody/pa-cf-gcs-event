# PA-CF-GCS-EVENT Cloud Function

## Overview
This cloud function, named `gcs_event_to_pubsub`, is designed to handle events from Google Cloud Storage (GCS). When specific GCS events occur, particularly concerning files with a certain naming pattern, this function triggers and publishes relevant information to a Google Pub/Sub topic.

The function operates as follows:

1. It listens to events from GCS.
2. Extracts the resource name from the incoming event.
3. Checks if the resource name (in this case, the file name) matches a desired pattern, which is primarily CSV files with a specific naming convention.
4. If the file name matches the pattern, it formats a message and publishes it to a Pub/Sub topic. If not, it logs that the resource failed the regex match.
5. For secure authentication and authorization purposes, the function utilizes impersonated credentials.

## Utilize the PA-CF Shared Configs Toolkit

Before diving into the deployment of this Cloud Function, it's vital to check out the [PA-CF Shared Configs Repository](https://github.com/acep-uaf/pa-cf-shared-configs). This valuable toolkit is designed to assist in efficiently setting up the necessary infrastructure, including creating service accounts, defining roles, and setting permissions. Using this toolkit will ensure a smooth and secure deployment of the Cloud Function, while minimizing manual configuration errors.

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
 
```bash
./pa_cf_gcs_event_deploy.sh
```

## Workflow

1. **gcloud command check**: The script first checks if the `gcloud` command-line tool is available on the system. If not, an error is raised.

```bash
if ! command -v gcloud &> /dev/null; then
    ...
fi
```

2. **gcloud authentication check**: The script then checks if the user is authenticated with `gcloud`.

```bash
gcloud auth list &> /dev/null
...
```

3. **.env file prompt**: The user is prompted to provide the path to an `.env` file that contains required environment variables.

```bash
echo "Enter the path to the .env file to use (e.g. ./myenvfile.env):"
read ENV_FILE
```

4. **.env file verification**: It checks if the provided .env file exists and is readable.

```bash
if [[ ! -f "$ENV_FILE" || ! -r "$ENV_FILE" ]]; then
    ...
fi
```

5. **Source .env file**: The .env file's variables are loaded into the script's environment.

```bash
source $ENV_FILE
```

6. **Environment Variable Checks**: The script checks if all the required environment variables are set. If any are missing, the deployment will not proceed.

```bash
declare -a required_vars=("GEN2" "RUNTIME" ... "SA_CREDENTIALS_SECRET_NAME")
...
```

7. **Cloud Function Deployment**: With all checks complete and the environment set up, the script deploys the Cloud Function using the `gcloud command`.

```bash
gcloud functions deploy pa-cf-gcs-event \
  --$GEN2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --service-account=$SERVICE_ACCOUNT \
  --source=$SOURCE \
  --entry-point=$ENTRY_POINT \
  --trigger-event-filters="$TRIGGER_EVENT_FILTERS" \
  --memory=$MEMORY \
  --timeout=$TIMEOUT \
  --set-env-vars "$SET_ENV_VARS"
  ```

## .env File Configuration
You should have an `deploy.env` file with the following variables defined:

```bash
GEN2=<value>
RUNTIME=<value>
REGION=<value>
SERVICE_ACCOUNT=<value>
SOURCE=<value>
ENTRY_POINT=<value>
TRIGGER_EVENT_FILTERS=<value>
MEMORY=<value>
TIMEOUT=<value>
PROJECT_ID=<value>
TOPIC_NAME=<value>
IMPERSONATE_SA=<value>
TARGET_SCOPES=<value>
SA_CREDENTIALS_SECRET_NAME=<value>
```

Replace `<value>` with the appropriate values for your deployment.

## Environment Variable Descriptions
Below are descriptions for each environment variable used in the deployment script:

- **GEN2**=`<value>`:
  - Description: Specifies the generation of the Cloud Function to deploy. For example: `gen2` when you intend to deploy a second generation Google Cloud Function.

- **RUNTIME**=`<value>`:
  - Description: Specifies the runtime environment in which the Cloud Function executes. For example: `python311` for Python 3.11.

- **REGION**=`<value>`:
  - Description: The Google Cloud region where the Cloud Function will be deployed and run. Example values are `us-west1`, `europe-west1`, etc.

- **SERVICE_ACCOUNT**=`<value>`:
  - Description: The service account under which the Cloud Function will run. This defines the permissions that the Cloud Function has during execution.

- **SOURCE**=`<value>`:
  - Description: Path to the source code of the Cloud Function. Typically, this points to a directory containing all the necessary files for the function.

- **ENTRY_POINT**=`<value>`:
  - Description: Specifies the name of the function or method within the source code to be executed when the Cloud Function is triggered.

- **TRIGGER_EVENT_FILTERS**=`<value>`:
  - Description: A comma-separated filter list to specify the type(s) of event that triggers the Cloud Function. For instance, it could denote specific types of changes in a GCS bucket, like "type=google.cloud.storage.object.v1.finalized,bucket=sw-pa-test".

- **MEMORY**=`<value>`:
  - Description: The amount of memory to allocate for the Cloud Function. This is denoted in megabytes, e.g., `16384MB`.

- **TIMEOUT**=`<value>`:
  - Description: The maximum duration the Cloud Function is allowed to run before it is terminated. Expressed in seconds, e.g., `540s`.

- **PROJECT_ID**=`<value>`:
  - Description: The Google Cloud Project ID where the Cloud Function, GCS, and Pub/Sub reside.

- **TOPIC_NAME**=`<value>`:
  - Description: The name of the Pub/Sub topic to which the Cloud Function will publish messages.

- **IMPERSONATE_SA**=`<value>`:
  - Description: The service account to impersonate for elevated tasks. The deploying service account impersonates this account when specific privileges are required.

- **TARGET_SCOPES**=`<value>`:
  - Description: The authentication scopes required for the impersonated service account. Example: `https://www.googleapis.com/auth/cloud-platform` for a full access scope to GCP services.

- **SA_CREDENTIALS_SECRET_NAME**=`<value>`:
  - Description: The name of the secret stored in Google Secret Manager that contains the service account credentials used by the Cloud Function.

### Dependencies
 
  The Cloud Function's dependencies are listed in the `requirements.txt` file and include:

  ```
  google-cloud-logging
  google-cloud-pubsub
  google-cloud-storage
  google-auth-httplib2
  google-auth-oauthlib
  google-cloud-secret-manager
  google-auth
  ```

## Conclusion

---
The `pa-cf-gcs-event` Cloud Function offers an efficient way to monitor and respond to Google Cloud Storage events, especially those concerning specific file naming patterns, by publishing them to a Google Pub/Sub topic. By leveraging Google Cloud's serverless capabilities, it ensures scalability without the need for extensive infrastructure management. Proper setup of environment variables and permissions, especially concerning service account impersonation, is paramount for security and function efficacy. The accompanying `pa_deploy.sh` script simplifies deployment, ensuring a streamlined implementation process for developers and cloud engineers.
