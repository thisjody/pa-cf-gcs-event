# PA-CF-GCS-EVENT Cloud Function

## Overview

The `pa-cf-gcs-event` Cloud Function is specifically designed to serve as an event-driven component in cloud-based data workflows, primarily focusing on responding to file events in Google Cloud Storage (GCS). It is finely tuned to trigger on specific GCS events, especially when files matching a predefined naming pattern are uploaded. The function's core operations are as follows:

1. **Event Listening**: Actively listens for file events from GCS, ready to respond to changes in storage.

2. **Pattern Recognition**: Upon receiving an event, it extracts the resource name (file name) and evaluates it against a set regex pattern, typically targeting CSV files with a specific naming convention.

3. **Selective Processing**: Only if the file name conforms to the expected pattern, the function proceeds to the next step. In cases where the file does not match, it logs the event for record-keeping and potential debugging purposes.

4. **Message Publication**: For files that meet the criteria, it formats and publishes a message to a designated Google Pub/Sub topic, thereby initiating subsequent processes in the data pipeline.

5. **Secure Operations**: The function incorporates impersonated credentials for heightened security, ensuring that operations are performed with appropriate authentication and authorization.

6. **Efficient and Scalable Processing**: Built to handle varying volumes and types of data, this function is a testament to efficiency and scalability, adapting seamlessly to different operational requirements within the cloud environment.

The `pa-cf-gcs-event` Cloud Function exemplifies a modern, event-driven approach in cloud computing, facilitating the automated and secure handling of storage events without intensive infrastructure management. Its integration into cloud-based workflows marks a significant step towards streamlined and efficient data processing in Google Cloud.

## Utilize the PA-CF Shared Configs Toolkit

Before diving into the deployment of this Cloud Function, it's vital to check out the [PA-CF Shared Configs Repository](https://github.com/acep-uaf/pa-cf-shared-configs). This valuable toolkit is designed to assist in efficiently setting up the necessary infrastructure, including creating service accounts, defining roles, and setting permissions. Using this toolkit will ensure a smooth and secure deployment of the Cloud Function, while minimizing manual configuration errors. Key aspects of the Shared Configs Toolkit include:

1. **Standardized Configuration**: The toolkit provides a set of standardized configurations that are essential for the consistent and error-free deployment of the cloud function.

2. **Efficient Setup**: It simplifies the setup process, reducing the complexity and time required to configure the necessary cloud resources and permissions.

3. **Security and Compliance**: By using predefined configurations, the toolkit helps in maintaining security standards and compliance, ensuring that the cloud function operates within the defined guidelines.

4. **Customization for Specific Needs**: While offering standard configurations, the toolkit also allows for necessary customizations specific to the `pa-cf-gcs-event` function. This includes setting up environment variables, defining roles, and permissions specific to the function's operation.

5. **Simplified Deployment Process**: The toolkit assists in the automated deployment of the cloud function, making it easier to manage and update without extensive manual intervention.

6. **Documentation and Support**: It provides comprehensive documentation and support, aiding in troubleshooting and ensuring that the function is set up correctly.

The integration with the PA-CF Shared Configs Toolkit is vital for ensuring that the `pa-cf-gcs-event` function is deployed efficiently, securely, and in a way that is consistent with the broader data processing infrastructure.

## Prerequisites
Before deploying and using this cloud function, ensure you have:

1. - **Google Cloud SDK**: Ensure the Google Cloud SDK is installed, as it provides tools to interact with Google Cloud resources. [Official Documentation](https://cloud.google.com/sdk/docs/install).
  
2. - **Google Cloud Project**: This function requires a Google Cloud Project where the Cloud Function, GCS, and Pub/Sub reside. Have the `PROJECT_ID` at hand.
  
3. - **Environment Variables**: The function utilizes several environment variables, such as:
    - `PROJECT_ID`: Your Google Cloud Project's ID.
    - `SA_CREDENTIALS_SECRET_NAME`: Secret name containing the service account credentials.
    - `IMPERSONATE_SA`: Service account to impersonate.
    - `TARGET_SCOPES`: Required scopes for the impersonated service account.

4. - **Google Secret Manager**: Store necessary secrets, like service account credentials.

5. - **Google Cloud Storage (GCS)**: This function reacts to GCS bucket events. Ensure a GCS bucket is set up and capable of generating events.

6. - **Google Pub/Sub**: Create a Pub/Sub topic for the function to publish messages. Set up the necessary permissions for publishing.

7. - **Permissions**: The function and its service account should have permissions for accessing Secret Manager, impersonating other service accounts, and publishing messages to Pub/Sub.

8. - **Cloud Storage Triggers Permission**: In order to use Cloud Storage triggers with Cloud Functions (2nd gen), ensure that the Cloud Storage service agent has the `roles/pubsub.publisher` IAM role on your project. This permission allows Cloud Storage to publish events to Pub/Sub, enabling the Cloud Function to trigger in response to file changes in the bucket. For detailed steps on setting this IAM role, refer to the [official documentation](https://cloud.google.com/functions/docs/calling/storage).

9. - **Enable IAM Service Account Credentials API**: To utilize service account impersonation features within the Cloud Function, the IAM Service Account Credentials API must be enabled in your Google Cloud Project. This API is crucial for allowing the deployment service account to impersonate another service account, ensuring secure and scoped access to Google Cloud resources. Enabling this API can be done through the Google Cloud Console or using the gcloud command-line tool. For more information and steps on enabling this API, please refer to [Enabling and Disabling Services](https://cloud.google.com/service-usage/docs/enable-disable).

9. **PA-CF Shared Configs Toolkit**: Familiarity with the PA-CF Shared Configs Toolkit is recommended for efficient setup and deployment.

Completing these prerequisites ensures that the `pa-cf-gcs-event` Cloud Function can be deployed smoothly and will operate as intended in your Google Cloud environment.

## Function Operation

The `pa-cf-gcs-event` Cloud Function is designed to handle and process events from Google Cloud Storage (GCS), especially focusing on files that match specific naming patterns. The operation of this function can be outlined in the following steps:

1. **Event Listening**:
   - The function is triggered by file-related events in GCS, such as the uploading of new files to a specified bucket.

2. **Extracting Information**:
   - Upon triggering, it extracts the resource name (the file name) from the event data.
   - Using the `extract_info` function, it then checks if the file name matches a predetermined regex pattern, which is primarily used to identify CSV files following a certain naming convention.

3. **Credentials Impersonation**:
   - For secure operations, the function utilizes impersonated credentials. It retrieves the necessary service account credentials for the 'publish' action from the Google Secret Manager.
   - This approach ensures that the function has the appropriate permissions to perform its tasks while adhering to security best practices.

4. **Data Publishing**:
   - If the file name matches the regex pattern, the function formats a message containing the type of file, bucket name, file name, and the extracted dataset and table names.
   - This message is then published to a specified Google Pub/Sub topic using the `publish_to_topic` function, facilitating the next steps in the data processing pipeline.

5. **Error Handling and Logging**:
   - The function includes robust error handling mechanisms. Any issues encountered during the operation, especially while publishing messages, are logged as errors.
   - Additionally, if a resource name does not match the desired pattern, the function logs a warning, providing visibility into files that are not processed.

6. **Scalability and Flexibility**:
   - Built to accommodate various file types and data volumes, the `pa-cf-gcs-event` function is highly scalable and flexible. It can easily adapt to different file naming conventions and patterns by adjusting the regex pattern.

This function operation flow showcases how `pa-cf-gcs-event` effectively acts as a gateway, filtering and forwarding relevant data from GCS to subsequent stages in the cloud-based data processing workflow.

## Functionality Overview

The `pa-cf-gcs-event` Cloud Function serves as a critical and dynamic component in the data processing pipeline, primarily focusing on handling events from Google Cloud Storage (GCS). Its functionalities encompass the following aspects:

1. **Event-Driven Processing**: This function is specially designed to respond to events in GCS, such as the uploading of new files. It serves as an event-driven gateway within the data processing workflow.

2. **Pattern Matching and Filtering**: Utilizing regular expressions, the function efficiently identifies files that match specific naming patterns. This selective processing ensures that only relevant data is forwarded in the pipeline.

3. **Message Publishing**: For files that meet the defined criteria, the function formats and publishes a structured message to a Google Pub/Sub topic. This action triggers downstream processes and facilitates a seamless data flow.

4. **Secure and Scalable Operations**: It employs impersonated credentials for secure access to cloud services, adhering to best practices in security and compliance. The function is designed to handle various data volumes, making it both scalable and reliable.

5. **Integration with Google Cloud Services**: The function seamlessly integrates with other Google Cloud services, such as Pub/Sub for message dissemination and Secret Manager for secure credential handling.

6. **Efficient Data Routing**: By analyzing and processing file events, the function plays a key role in routing data to appropriate destinations, such as triggering data loading functions or other processing units.

7. **Robust Error Handling and Logging**: The function includes comprehensive error handling capabilities, ensuring any issues are promptly logged and addressed. This robust logging mechanism aids in monitoring and maintaining the function's performance.

The `pa-cf-gcs-event` Cloud Function is thus an essential component in cloud-based data processing ecosystems, offering efficient, secure, and intelligent handling of GCS events to streamline the data management lifecycle.

## Error Handling

The `pa-cf-gcs-event` Cloud Function incorporates comprehensive error handling mechanisms to maintain its reliability and effectiveness, even when confronted with unforeseen challenges. These mechanisms are strategically designed to detect, log, and appropriately manage various types of errors that might occur during the function's execution:

1. **Logging of Exceptions**: All exceptions and errors encountered during the operation of the function are logged with detailed information. This includes errors during dataset and table creation, data loading, or while interacting with other cloud services.

2. **Handling Google Cloud API Errors**: Specific errors related to Google Cloud APIs, such as `NotFound` and `Forbidden` exceptions, are caught and handled. This ensures that the function can gracefully handle issues such as missing resources or permission problems.

3. **Error Propagation**: In cases where errors cannot be resolved within the function (e.g., permission issues, invalid configurations), these errors are propagated upwards. This allows for external monitoring tools or workflows to detect and respond to these issues.

4. **Secure Failure State**: In scenarios where continued operation could lead to data inconsistency or other critical issues, the function is designed to fail securely. This approach prioritizes data integrity and system stability.

5. **Alerting and Monitoring Integration**: The function's error handling integrates with Google Cloud's monitoring and alerting systems, enabling real-time notifications and in-depth analysis of error conditions.

These error handling approaches ensure that the `pa-cf-gcs-event` Cloud Function remains a robust and dependable component in handling GCS events, capable of adapting to and overcoming various operational challenges.


## Dependencies

The `pa-cf-gcs-event` Cloud Function depends on a range of external libraries and services to function effectively. These dependencies encompass various Python packages and Google Cloud services. The key dependencies are as follows:

1. **Google Cloud Pub/Sub**: Integral for publishing messages to Pub/Sub topics, which is a core part of the function's operation.

2. **Google Cloud Storage**: Although not directly interacted with by the function, it is crucial for triggering the function through file events in GCS buckets.

3. **Google Secret Manager**: Used for securely managing and accessing sensitive information such as service account credentials.

4. **Python Libraries**:
    - `google-cloud-pubsub`: The Python client library for Google Cloud Pub/Sub, enabling the function to publish messages to Pub/Sub topics.
    - `google-cloud-secret-manager`: Used for accessing secrets stored in Google Secret Manager, critical for managing secure credentials.
    - `google-auth`, `google-auth-httplib2`, and `google-auth-oauthlib`.
    
     These libraries provide authentication functionalities, essential for interacting securely with Google Cloud services and are listed in `requirements.txt` .

5. **Regular Expression Processing**:
    - The function uses Python's built-in `re` module for regex operations, crucial for pattern matching in file names.

6. **Logging and Error Handling**:
    - `logging`: A standard Python library used for logging events, errors, and informational messages, aiding in debugging and monitoring the function's operation.

It is important to have these dependencies correctly installed and configured to ensure smooth operation of the `pa-cf-gcs-event` Cloud Function. Proper setup helps prevent runtime errors and ensures that the function performs as intended within the cloud environment.

## Roles and Service Accounts

The `PA-CF-GCS-EVENT` Cloud Function utilizes the [PA-CF Shared Configs Toolkit](https://github.com/acep-uaf/pa-cf-shared-configs) for standardized and secure configuration of service accounts. This toolkit simplifies the process of deploying and managing cloud functions by providing a consistent approach to service account setup and permissions management.

### Service Accounts

The function employs specific service accounts for its operation, each tailored to perform distinct roles:

1. **Deploy Service Account (`$SERVICE_ACCOUNT`)**:
   - This service account is primarily used for deploying the Cloud Function.
   - It is configured to have minimal permissions necessary for the deployment process. After deployment, it can impersonate other service accounts for executing specific tasks, thereby adhering to the principle of least privilege.
   - The configuration details of this account are managed via the shared configs, ensuring a secure and controlled deployment.

2. **Publish Service Account (`$PUBLISH_SA`)**:
   - Utilized for operations related to publishing messages to Google Cloud Pub/Sub, a crucial aspect of the function's role in responding to GCS events.
   - The permissions and setup of this account are defined within the shared configs, aligning it with the function's requirements and security protocols.

The use of these service accounts, as dictated by the PA-CF Shared Configs Toolkit, allows the `PA-CF-GCS-EVENT` Cloud Function to maintain high standards of security and efficiency. The toolkit ensures that service accounts are appropriately configured for their respective roles in the function's lifecycle. For more detailed information on the service accounts' configuration, please refer to the [PA-CF Shared Configs Toolkit](https://github.com/acep-uaf/pa-cf-shared-configs).


## Deployment Script for PA-CF-GCS-EVENT Cloud Function

The `pa_cf_gcs_event_deploy.sh` script simplifies the deployment of the pa-cf-gcs-event Cloud Function by automating the process, ensuring the necessary prerequisites are met, and setting up the correct environment variables for deployment.

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
gcloud functions deploy $CLOUDFUNCTION \
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
CLOUDFUNCTION=<value>
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

- **CLOUDFUNCTION**=`<value>`:
   - Description: The name of the Cloud Function to be deployed. It is used in the deployment script to identify which function the `gcloud functions deploy` command will target.

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

## Conclusion

---
The `pa-cf-gcs-event` Cloud Function offers an efficient way to monitor and respond to Google Cloud Storage events, especially those concerning specific file naming patterns, by publishing them to a Google Pub/Sub topic. By leveraging Google Cloud's serverless capabilities, it ensures scalability without the need for extensive infrastructure management. Proper setup of environment variables and permissions, especially concerning service account impersonation, is paramount for security and function efficacy. The accompanying `pa_deploy.sh` script simplifies deployment, ensuring a streamlined implementation process for developers and cloud engineers.
