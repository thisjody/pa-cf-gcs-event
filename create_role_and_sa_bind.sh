#!/bin/bash

# Set project ID
PROJECT_ID="acep-ext-eielson-2021"

# Set the name of the custom role
ROLE_NAME="custom_role_pa_cf_gcs_event"

# Set the path to the role definition file
ROLE_FILE="custom_role.json"

# Set the name and email of the service account
SA_NAME="pa-cf-gcs-event-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Check if the role exists
ROLE_EXISTS=$(gcloud iam roles describe $ROLE_NAME --project=$PROJECT_ID 2>&1 | grep "name:")

if [ -z "$ROLE_EXISTS" ]; then
    # Create the custom role
    gcloud iam roles create $ROLE_NAME --project=$PROJECT_ID --file=$ROLE_FILE --quiet
    echo "Custom role $ROLE_NAME has been created in project $PROJECT_ID."
else
    # Update the custom role
    gcloud iam roles update $ROLE_NAME --project=$PROJECT_ID --file=$ROLE_FILE --quiet
    echo "Custom role $ROLE_NAME has been updated in project $PROJECT_ID."
fi

# Check if the service account exists
SA_EXISTS=$(gcloud iam service-accounts describe $SA_EMAIL 2>&1 | grep "email:")

if [ -z "$SA_EXISTS" ]; then
    # Create the service account
    gcloud iam service-accounts create $SA_NAME --display-name $SA_NAME --project=$PROJECT_ID --quiet
    echo "Service account $SA_NAME has been created."
fi

# Check if the role is bound to the service account
ROLE_BOUND=$(gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format='table(bindings.role,bindings.members)' | grep $SA_EMAIL | grep $ROLE_NAME)

if [ -z "$ROLE_BOUND" ]; then
    # Bind the role to the service account
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="projects/$PROJECT_ID/roles/$ROLE_NAME" --quiet
    echo "Custom role $ROLE_NAME has been bound to service account $SA_NAME."
fi