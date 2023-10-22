import uuid

from db import connection

RANGES = [
    {
        "name": "baixíssimo",
        "start_value": 0,
        "end_value": 0.49999
    },
    {
        "name": "baixo",
        "start_value": 0.5,
        "end_value": 0.99999
    },
    {
        "name": "mediano",
        "start_value": 1,
        "end_value": 2.99999
    },
    {
        "name": "alto",
        "start_value": 3,
        "end_value": 3.99999
    },
    {
        "name": "altíssimo",
        "start_value": 4,
        "end_value": 5
    }
]

def save_infractions_by_match_average_ranges():
    for passes in RANGES:
        connection.exec_driver_sql(
            "INSERT INTO infractions_by_match_average_range (id, name, start_value, end_value) "
            "VALUES (%(id)s, %(name)s, %(start_value)s, %(end_value)s) "
            "ON CONFLICT(name) "
            "DO NOTHING",
            {
                "id": uuid.uuid4(),
                "name": passes["name"],
                "start_value": passes["start_value"],
                "end_value": passes["end_value"],
            }
        )
    connection.commit()
