from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Operator

passw = "p!32Mz?Wt59X~[kC"
url = f'postgresql://postgres:postgres@/postgres?host=postgres'
engine = create_engine(url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def init_admin_user():
    pwd_context = CryptContext(schemes=["argon2"])
    password_hashed = pwd_context.hash("Windows8")
    basic_admin = User(email="stefan.drobic@vizlore.com", password=password_hashed)

    db.add(basic_admin)
    db.commit()

# def init_operator (>, <, ...)
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
    init_admin_user()
    init_operators()
    db.flush()
    db.close()
    print("init_db done")


if __name__ == "__main__":
    init_db()
