#!/bin/bash

# Source the .env file
source pa_deploy.env

# Formulate the SET_ENV_VARS value
SET_ENV_VARS="PROJECT_ID=$PROJECT_ID,TOPIC_NAME=$TOPIC_NAME,IMPERSONATE_SA=$IMPERSONATE_SA,TARGET_SCOPES=$TARGET_SCOPES,SA_CREDENTIALS_SECRET_NAME=$SA_CREDENTIALS_SECRET_NAME"

# Deploy the function
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
