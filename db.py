import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+psycopg2://postgres:1234@localhost/soccer_datawarehouse')
data_frame = pd.read_csv("main-dataset.csv")
engine = create_engine(DATABASE_URL, pool_recycle=3600)
connection = engine.connect()
