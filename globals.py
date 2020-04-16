from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}", echo=True)
Base = declarative_base()