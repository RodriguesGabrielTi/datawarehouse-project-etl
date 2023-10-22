import uuid

from pandas import DataFrame

from db import connection


def save_teams(main_df: DataFrame):
    for index, row in main_df.iterrows():
        random_id = uuid.uuid4()
        team = {
            "id": random_id,
            "source_id": row["Club_x_id"],
            "name": row["Club_x"],
        }
        connection.exec_driver_sql(
            "INSERT INTO team (id, source_id, name) "
            "VALUES (%(id)s, %(source_id)s, %(name)s) "
            "ON CONFLICT(source_id) "
            "DO UPDATE SET name = %(name)s",
            team
        )
    connection.commit()
