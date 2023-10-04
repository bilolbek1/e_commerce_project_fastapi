from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///e_commerce_db', echo=True)



Base = declarative_base()
Session = sessionmaker()