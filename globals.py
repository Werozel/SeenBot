from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine("postgresql://{db_username}:{db_password}@{db_host}/{db_name}")
Base = declarative_base()