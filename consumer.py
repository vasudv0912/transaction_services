from kafka import KafkaConsumer
from sqlalchemy.orm import sessionmaker
from multiprocessing import Process
import json
import sqlalchemy
from models import Transaction, Wallet
from kafka import KafkaProducer
import json

bootstrap_servers = ['172.17.0.1:9091']
engine = sqlalchemy.create_engine(
    'mysql://transaction:osmentos@mysqltransdb:3306/transaction', echo=True)


def value_deserializer(m): return json.loads(m.decode('utf-8'))


Session = sessionmaker(bind=engine)
session = Session()


def transaction():
    try:
        consumer = KafkaConsumer(
            'transaction', bootstrap_servers=bootstrap_servers, value_deserializer=value_deserializer)
    except Exception as e:
        print(str(e))

    for message in consumer:
        print(message.value)
        wallet_from = session.query(Wallet).filter_by(
            user_id=message.value['_from']).first()
        amount = message.value['amount']
        if wallet_from.balance >= amount:
            ed = Transaction(_to=message.value['_to'], _from=message.value['_from'],
                             record_id=message.value['record_id'], amount=message.value['amount'])
            session.add(ed)
            session.commit()
            wallet_from.balance -= amount
            session.commit()
            wallet_to = session.query(Wallet).filter_by(
                user_id=message.value['_to']).first()
            wallet_to.balance += amount
            session.commit()

            topicName = 'change_status'
            producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(
                topicName, {'current_owner_id': ed._from, 'record_id': ed.record_id})
            producer.flush()
        else:
            pass


Process(target=transaction).start()


def wallet():
    try:
        consumer = KafkaConsumer(
            'wallet', bootstrap_servers=bootstrap_servers, value_deserializer=value_deserializer)
    except Exception as e:
        print(str(e))

    for message in consumer:
        print(message.value)
        ed = Wallet(user_id=message.value['user_id'],
                    balance=message.value['balance'])
        session.add(ed)
        session.commit()


Process(target=wallet).start()
