from sqlalchemy import create_engine
import config

engine = create_engine("postgresql://{db_username}:{db_password}@{db_host}/{db_name}")