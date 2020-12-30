from google.cloud import storage
from google.cloud import pubsub_v1
import smtplib 
import json
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from flask import jsonify


def send_mail(request):

    request_data = json.loads(request.get_data())
    if request_data:
        pdf = request_data['pdf']
        email = request_data['mail']
    else:
        return format("Undone")
    fromaddr = "text2pdfconverter@gmail.com"

    # *****Access pdf from bucket*******************
    bucket_name = "gcf-sources-353018688455-us-central1"
    source_blob_name = pdf
    destination_file_name = "/tmp/text2pdf.pdf"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    
    # ******Create content for mail*****************
    msg = MIMEMultipart() 
      
    msg['From'] = fromaddr  
    msg['To'] = email 
    msg['Subject'] = "Here's your PDF"
    body = "PFA your PDF"
    msg.attach(MIMEText(body, 'plain')) 
    
    filename = destination_file_name
    attachment = open(filename, "rb") 
    
    p = MIMEBase('application', 'octet-stream') 
    
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % pdf) 
     
    msg.attach(p) 
    
    # ******Send mail*****************
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    
    s.login(fromaddr, "****") 

    text = msg.as_string() 
    
    s.sendmail(fromaddr, email, text) 
    s.quit()

    project_id = "manisha-suresh"
    topic_id = "cleanup"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    messageID = publisher.publish(topic_path, pdf.split('.')[0].encode("utf-8"))

    response = jsonify({"mail_sent" : 1})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
