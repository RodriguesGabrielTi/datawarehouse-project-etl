import uuid

from pandas import DataFrame

from db import connection


def save_leagues(main_df: DataFrame):
    for index, row in main_df.iterrows():
        random_id = uuid.uuid4()
        league = {
            "id": random_id,
            "source_id": row["League_id"],
            "name": row["League"],
        }
        connection.exec_driver_sql(
            "INSERT INTO league (id, source_id, name) "
            "VALUES (%(id)s, %(source_id)s, %(name)s) "
            "ON CONFLICT(source_id) "
            "DO NOTHING",
            league
        )
    connection.commit()
