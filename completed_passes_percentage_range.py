import uuid

from db import connection

RANGES = [
    {
        "name": "baixíssimo",
        "start_value": 0,
        "end_value": 0.3999
    },
    {
        "name": "baixo",
        "start_value": 0.4,
        "end_value": 0.5999
    },
    {
        "name": "mediano",
        "start_value": 0.6,
        "end_value": 0.6999
    },
    {
        "name": "alto",
        "start_value": 0.7,
        "end_value": 0.8499
    },
    {
        "name": "altíssimo",
        "start_value": 0.85,
        "end_value": 1
    }
]

def save_passes_range():
    for passes in RANGES:
        connection.exec_driver_sql(
            "INSERT INTO completed_passes_percentage_range (id, name, start_value, end_value) "
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
