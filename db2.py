from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL="sqlite:///./items.db"

engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
metadata=MetaData()
Base=declarative_base()
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)