from database import Base, engine
from models import User, Product

Base.metadata.create_all(bind=engine)
