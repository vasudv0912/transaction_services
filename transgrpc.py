from grpcalchemy import DefaultConfig
from models import Wallet
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from grpcalchemy.orm import Message, StringField
from grpcalchemy import Server, Context, grpcmethod

engine = sqlalchemy.create_engine(
    'mysql://transaction:osmentos@mysqltransdb:3306/transaction', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class TransRequestMesg(Message):
    user_id: int


class TransResponseMesg(Message):
    amount: int


class TransactionServices(Server):
    @grpcmethod
    def getBalance(self, request: TransRequestMesg, context: Context) -> TransResponseMesg:
        balance = session.query(Wallet).filter_by(
            id=request.user_id).first()
        return TransResponseMesg(amount=balance.balance)


class TestConfig(DefaultConfig):
    GRPC_SEVER_REFLECTION_ENABLE = True


if __name__ == '__main__':
    TransactionServices.run(host="transaction", port=5007, config=TestConfig())
