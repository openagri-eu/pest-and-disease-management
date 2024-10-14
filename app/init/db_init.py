from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Operator

from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def init_operators():
    a = Operator(symbol=">")
    c = Operator(symbol="<")
    d = Operator(symbol=">=")
    e = Operator(symbol="<=")
    f = Operator(symbol="==")
    g = Operator(symbol="!=")

    l = [a,c,d,e,f,g]
    for operator in l:
        db.add(operator)
        db.commit()



def init_db():
    init_operators()
    db.flush()
    db.close()
