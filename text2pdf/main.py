import base64
from google.cloud import storage
from fpdf import FPDF 

def text2pdf(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    destination_blob_name = pubsub_message + '.pdf'
    # print(destination_blob_name)

    storage_client = storage.Client()
    bucket_name = "gcf-sources-353018688455-us-central1"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(pubsub_message)
    blob.download_to_filename('/tmp/text_file.txt')

    pdf = FPDF()    
    pdf.add_page()  
    pdf.set_font("Arial", size = 15) 
    f = open("/tmp/text_file.txt", "rb") 
    for x in f: 
        x = x.decode('latin-1', errors='ignore')
        pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 
    
    pdf.output("/tmp/text2pdf.pdf")    
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename("/tmp/text2pdf.pdf")
