from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}")
SessionFactory = sessionmaker()
SessionFactory.configure(bind=engine, autocommit=True)
session = SessionFactory()
Base = declarative_base()