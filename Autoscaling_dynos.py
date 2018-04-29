import boto3
import botocore
import os

print("**************************************************")
print("Inicia controlador del autoscaling para el worker ")
print("**************************************************")

access_id=os.environ["S3_AWS_ACCESS_KEY_ID"]
access_secret=os.environ["S3_AWS_SECRET_ACCESS_KEY"]
sqs = boto3.resource('sqs', aws_access_key_id=access_id, aws_secret_access_key=access_secret)
queue = sqs.get_queue_by_name(QueueName='sqs_concursos')
url_queue=queue.url
print("Conectado a la url: ", url_queue)
while True:
    total_mensajes=queue.ApproximateNumberOfMessages
    print(total_mensajes)
