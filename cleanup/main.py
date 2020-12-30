import base64
from google.cloud import storage

def cleanup(event, context):

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    destination_blob_name = pubsub_message
    destination_blob_name2 = pubsub_message + '.pdf'

    storage_client = storage.Client()
    bucket_name = "gcf-sources-353018688455-us-central1"
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.delete()

    blob = bucket.blob(destination_blob_name2)
    blob.delete()    
