import uuid
from math import ceil

import pandas as pd
from pandas import DataFrame
import numpy as np

from db import connection


class FrequencyDimensionCalc:
    def __init__(self):
        self._percentages = [("baixíssimo", 0.1), ("baixo", 0.3), ("normal", 0.6), ("alto", 0.8), ("altissímo", 1)]

    def update_all_players(self):
        connection.exec_driver_sql(
            "UPDATE player_fact SET"
            "   goals_frequency_range_id = (SELECT id FROM goals_frequency_range WHERE start_value <= goals_per_match::int AND end_value >= goals_per_match::int LIMIT 1),"
            "   assists_frequency_range_id = (SELECT id FROM assists_frequency_range WHERE start_value <= assists_per_90_min::int AND end_value >= assists_per_90_min::int LIMIT 1)"
        )
        connection.commit()

    def compute_goals(self, dataframe: DataFrame):
        df = pd.DataFrame({'values': dataframe["Goals by match"].values})
        dimensions = self.execute(df)
        if not dimensions:
            return
        ids = []
        for dimension_key in dimensions:
            id =  uuid.uuid4()
            connection.exec_driver_sql(
                "INSERT INTO goals_frequency_range (id, name, start_value, end_value) "
                "VALUES (%(id)s, %(name)s, %(start_value)s, %(end_value)s) ",
                {
                    "id": id,
                    "name": dimensions[dimension_key]["name"],
                    "start_value": float(dimensions[dimension_key]["min_value"]) if dimensions[dimension_key]["min_value"] != 5e-324 else 0,
                    "end_value": float(dimensions[dimension_key]["max_value"]),
                }
            )
            ids.append(str(id))
        formatted_ids = ",".join(["'{}'::uuid".format(id) for id in ids])
        sql = f"DELETE FROM goals_frequency_range WHERE id not in (SELECT unnest(ARRAY[{formatted_ids}]))"
        connection.exec_driver_sql(sql)
        connection.commit()

    def compute_assists(self, dataframe: DataFrame):
        df = pd.DataFrame({'values': dataframe["Assists by match"].values})
        dimensions = self.execute(df)
        if not dimensions:
            return
        ids = []
        for dimension_key in dimensions:
            id =  uuid.uuid4()
            connection.exec_driver_sql(
                "INSERT INTO assists_frequency_range (id, name, start_value, end_value) "
                "VALUES (%(id)s, %(name)s, %(start_value)s, %(end_value)s) ",
                {
                    "id": id,
                    "name": dimensions[dimension_key]["name"],
                    "start_value": dimensions[dimension_key]["min_value"]  if dimensions[dimension_key]["min_value"] != 5e-324 else 0,
                    "end_value": dimensions[dimension_key]["max_value"],
                }
            )
            ids.append(str(id))
        formatted_ids = ",".join(["'{}'::uuid".format(id) for id in ids])
        sql = f"DELETE FROM assists_frequency_range WHERE id not in (SELECT unnest(ARRAY[{formatted_ids}]))"
        connection.exec_driver_sql(sql)
        connection.commit()

    def execute(self, df: DataFrame):
        dimensions_by_percentage_position = {}
        if 'values' not in df.columns:
            raise ValueError("Dataframe needs values to compute")
        interactions_orderly = pd.array(df["values"].sort_values())
        if not interactions_orderly:
            return
        next_value = None
        for name, percentage in self._percentages:
            max_value_position = ceil(interactions_orderly.size * percentage) - 1
            max_value = interactions_orderly[max_value_position]
            min_value = next_value if next_value else 0
            dimensions_by_percentage_position.update({
                percentage: {
                    'min_value': min_value,
                    'max_value': max_value,
                    'name': name
                }
            })
            try:
                next_value = np.nextafter(max_value, np.inf) if isinstance(max_value, np.float64) else max_value + 1
            except IndexError:
                next_value = None
        return dimensions_by_percentage_position