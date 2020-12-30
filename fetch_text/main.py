import urllib
import urllib.request
import collections
import requests
import json
from google.cloud import storage
from flask import jsonify
import time
from google.cloud import pubsub_v1

def fetch_text(request):

    text_url = json.loads(request.get_data())
    if text_url:
        url = text_url['url']
    else:
        return format("Undone")

    storage_client = storage.Client()
    bucket_name = "gcf-sources-353018688455-us-central1"
    bucket = storage_client.bucket(bucket_name)
    destination_blob_name = url.split('/')[-1].split('.')[0]
    
    file = urllib.request.urlopen(url).read()
    if not file:
        return format("Undone")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file)

    project_id = "manisha-suresh"
    topic_id = "text_dumped"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    messageID = publisher.publish(topic_path, destination_blob_name.encode("utf-8"))
    
    blob = bucket.blob(destination_blob_name + '.pdf')
    while not blob.exists(storage_client):
        continue

    response = jsonify({"textFileName" : destination_blob_name + '.pdf'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
