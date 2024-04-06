import pika, json, os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dash.settings')
django.setup()

from rest_framework.response import Response
from rest_framework import status
from product.models import Product

params = pika.URLParameters('replace with your credentials')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, prop, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    try:
        product = Product.objects.get(id=id)
        product.likes = product.likes + 1
        product.save()
        print('Product liked')
    except Product.DoesNotExist:
        return Response({"error":"no product found"}, status=status.HTTP_400_BAD_REQUEST)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('started consuming')

channel.start_consuming()
channel.close()
