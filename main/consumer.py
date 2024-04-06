import pika
import json
from main import app
from main import Product, db


params = pika.URLParameters('replace with your credentials')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

with app.app_context():
    def callback(ch, method, proprties, body):
        print('Received in main')
        data = json.loads(body)
        print(data)
        print(proprties)
        if proprties.content_type == 'product_created':
            product = Product(
                id=data['id'], title=data['title'], image=data['image']
            )
            db.session.add(product)
            db.session.commit()
        elif proprties.content_type == 'product_updated':
            try:
                product = Product.query.get(data['id'])
                product.title = data['title']
                product.image = data['image']
                db.session.commit()
            except Exception as e:
                print(e)
                pass
        elif proprties.content_type == 'product_deleted':
            try:
                product = Product.query.get(data)
                db.session.delete(product)
                db.session.commit()
            except Exception as e:
                print(e)
                pass


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('started consuming')

channel.start_consuming()
channel.close()
