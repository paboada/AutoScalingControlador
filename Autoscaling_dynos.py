import boto3
import botocore
import os
import time

print("**************************************************")
print("Inicia controlador del autoscaling para el worker ")
print("**************************************************")

print("Digite el numero de mensajes limite para escalar el dyno del worker")
limite_mensajes=input()
num_max_dinos=2
dynos_iniciales=1

while True:
    access_id=os.environ["S3_AWS_ACCESS_KEY_ID"]
    access_secret=os.environ["S3_AWS_SECRET_ACCESS_KEY"]
    sqs_cliente = boto3.client('sqs', aws_access_key_id=access_id, aws_secret_access_key=access_secret)
    sqs = boto3.resource('sqs', aws_access_key_id=access_id, aws_secret_access_key=access_secret)
    queue = sqs.get_queue_by_name(QueueName='sqs_concursos')
    url_queue=queue.url
    print("Conectado a la url: ", url_queue)

    total_mensajes=queue.attributes
    #print(total_mensajes["ApproximateNumberOfMessages"])
    if int(total_mensajes["ApproximateNumberOfMessages"])>int(limite_mensajes) and dynos_iniciales<num_max_dinos:
        print("ALERTA!!!!!!! se sobrepaso el limite de mensajes en la cola")
        print("Debe escalarse el dyno del Worker!!!!!!!!!")
        print("Ejecutanto sentencia heroku")
        os.system('heroku ps:scale --app "salty-wave-46611" worker=2')
        print("Dyno escalado, revisar!!!!!")
        dynos_iniciales=dynos_iniciales+1
    if int(total_mensajes["ApproximateNumberOfMessages"])<int(limite_mensajes):
        print("Limite normal de mensajes")
        print("Maximo numero de mensajes elegido: ", limite_mensajes )
        print("Mensajes en la cola: ", int(total_mensajes["ApproximateNumberOfMessages"]))
        if dynos_iniciales == 2:
            print("Se debe decrementar 1 dyno")
            os.system('heroku ps:scale --app "salty-wave-46611" worker=1')
            dynos_iniciales=dynos_iniciales-1

    time.sleep(5)
    print("**************************************************")
    print("**************************************************")
