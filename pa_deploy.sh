gcloud functions deploy pa-cf-gcs-event \
  --gen2 \
  --runtime=python311 \
  --region=us-west1 \
  --service-account=pa-cf-deploy-sa@acep-ext-eielson-2021.iam.gserviceaccount.com \
  --source=src \
  --entry-point=gcs_event_to_pubsub \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=sw-pa-test" \
  --memory 16384MB \
  --timeout 540s  \
  --set-env-vars PROJECT_ID=acep-ext-eielson-2021,TOPIC_NAME=pa-gcs-event,IMPERSONATE_SA=pa-gcs-ps-privileged-sa@acep-ext-eielson-2021.iam.gserviceaccount.com,TARGET_SCOPES="https://www.googleapis.com/auth/cloud-platform"