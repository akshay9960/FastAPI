from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url= "postgresql://A200228813@localhost:5432/my_fastapi_db"

engine=create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)