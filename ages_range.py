import uuid
import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+psycopg2://postgres:1234@localhost/soccer_datawarehouse')
data_frame = pd.read_csv("main-dataset.csv")
engine = create_engine(DATABASE_URL, pool_recycle=3600)
connection = engine.connect()

AGE_RANGE = [
    {
        "name": "PROMISING_YOUNG",
        "start_value": 0,
        "end_value": 23
    },
    {
        "name": "MATURATION",
        "start_value": 24,
        "end_value": 28
    },
    {
        "name": "CAREER_PEAK",
        "start_value": 29,
        "end_value": 32
    },
    {
        "name": "END_OF_CAREER",
        "start_value": 33,
        "end_value": 38
    },
    {
        "name": "VETERAN",
        "start_value": 39,
        "end_value": 100
    }
]

def save_ages_range():
    for age in AGE_RANGE:
        connection.exec_driver_sql(
            "INSERT INTO age_range (id, name, start_value, end_value) "
            "VALUES (%(id)s, %(name)s, %(start_value)s, %(end_value)s) "
            "ON CONFLICT(name) "
            "DO UPDATE SET start_value = %(start_value)s, end_value = %(end_value)s",
            {
                "id": uuid.uuid4(),
                "name": age["name"],
                "start_value": age["start_value"],
                "end_value": age["end_value"],
            }
        )
    connection.commit()
