from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# This might not be the right way to import
#from config import database_uri

engine = create_engine(app.config[“SQLALCHEMY_DATABASE_URI”])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)