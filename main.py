from pandas import DataFrame
from sqlalchemy import create_engine
import os
import psycopg2

import pandas as pd

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+psycopg2://postgres:1234@localhost/soccer_datawarehouse')
# Create a DataFrame
data_frame = pd.read_csv("main-dataset.csv")
engine = create_engine(DATABASE_URL, pool_recycle=3600)
connection = engine.connect()

soccer_table = "soccer"

def create_soccer_dataframe(main_df: DataFrame) -> DataFrame:
    return main_df

soccer_dataframe = create_soccer_dataframe(main_df=data_frame)
try:
    frame = data_frame.to_sql(soccer_table, connection, if_exists='fail')
except ValueError as vx:
    print(vx)
except Exception as ex:
    print(ex)

print("PostgreSQL Table %s has been created successfully." % soccer_table)
connection.close()
