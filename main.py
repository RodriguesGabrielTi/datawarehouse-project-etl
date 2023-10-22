import uuid

from dateutil.utils import today
from numpy import NaN
from pandas import DataFrame
from sqlalchemy import create_engine
import os

import pandas as pd

from ages_range import save_ages_range
from completed_passes_percentage_range import save_passes_range
from frequency_dimension_calc import FrequencyDimensionCalc
from infractions_by_match_average_range import save_infractions_by_match_average_ranges
from league import save_leagues
from overall_player_points import calc_overall_player_points
from team import save_teams
from utils import extract_float

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+psycopg2://postgres:1234@localhost/soccer_datawarehouse')
data_frame = pd.read_csv("main-dataset.csv")
engine = create_engine(DATABASE_URL, pool_recycle=3600)
connection = engine.connect()

soccer_table = "soccer"
BATCH_DATE = today().date()

def clean_dataframe(data: DataFrame) -> DataFrame:
    data = data.fillna(value=0)
    data["Market value"] = data["Market value"].apply(lambda x: extract_float(x))
    data.drop(data[data["Age"] == 0].index, inplace=True)
    data.drop(data[data["MP"] == 0].index, inplace=True)
    data["Gls"] = data["Gls"].astype(int)
    return data.fillna(0)


def save_positions(data: DataFrame):
    positions = data["Pos"].unique()
    unique_positions = set()
    for position in positions:
        if "," not in str(position):
            unique_positions.add(position)
            continue
        unique_positions.update(set(position.split(",")))

    for position in unique_positions:
        random_uuid = uuid.uuid4()
        connection.exec_driver_sql(
            "INSERT INTO position "
            "(id, name) "
            "VALUES (%(id)s, %(name)s) "
            "ON CONFLICT(name) "
            "DO NOTHING",
            {"id": random_uuid, "name": position}
        )
    connection.commit()


def add_column_infractions(data: DataFrame) -> DataFrame:
    """
    Cria nova coluna "Infractions" soma de cartoes armarelos e vermelhos,
    sendo cartoes amarelos valendo 1 ponto e vermelhos valendo 2 pontos
    """
    infractions = []
    for index, row in data.iterrows():
        infraction_value = int(row["CrdY"]) + int(row["CrdR"] * 2)
        infractions.append(infraction_value)
    data["Infractions"] = infractions
    return data


def add_column_infractions_by_match(data: DataFrame) -> DataFrame:
    """
    Cria nova coluna "Infractions by match" soma de cartoes armarelos e vermelhos,
    sendo cartoes amarelos valendo 1 ponto e vermelhos valendo 2 pontos. O valor máximo é 5
    """
    infractions_by_match_values = []
    for index, row in data.iterrows():
        infractions = row["Infractions"]
        infractions_by_match = infractions / row["MP"] if row["MP"] else 0
        infractions_by_match_values.append(min(infractions_by_match, 5))
    data["Infractions by match"] = infractions_by_match_values
    return data


def add_goals_by_match(data: DataFrame) -> DataFrame:
    """
    Cria nova coluna "Goals by match" contabilizando a média de gols por partida
    """
    values = []
    for index, row in data.iterrows():
        value = row["Gls"]
        goals_by_match = value / row["MP"] if row["MP"] else 0
        values.append(goals_by_match)
    data["Goals by match"] = values
    return data


def add_assists_by_match(data: DataFrame) -> DataFrame:
    """
    Cria nova coluna "Assists by match" contabilizando a média de assistências por partida
    """
    values = []
    for index, row in data.iterrows():
        value = row["Ast"]
        assists_by_match = value / row["MP"] if row["MP"] else 0
        values.append(assists_by_match)
    data["Assists by match"] = values
    return data


def add_overall_point_column(data: DataFrame) -> DataFrame:
    """
    Cria nova coluna "Overall point" calculo de pontuação de performance do jogador
    """
    overall_point_values = []
    for index, row in data.iterrows():
        overall_point = calc_overall_player_points(row)
        overall_point_values.append(overall_point)
    data["Overall point"] = overall_point_values
    return data


def save_players_profiles(data: DataFrame):
    for index, row in data.iterrows():
        random_uuid = uuid.uuid4()
        connection.exec_driver_sql(
            "INSERT INTO player_profile "
            "(id, source_id, name, age, nation) "
            "VALUES (%(id)s, %(source_id)s, %(name)s, %(age)s, %(nation)s) "
            "ON CONFLICT(source_id) DO "
            "UPDATE SET name = %(name)s, age = %(age)s, nation = %(nation)s",
            {
                "id": random_uuid,
                "source_id": row["id"],
                "age": int(row["Age"]),
                "name": row["Player"],
                "nation": row["Nation"]
            }
        )
    connection.commit()


def save_players(data: DataFrame):
    for index, row in data.iterrows():
        connection.exec_driver_sql(
            "INSERT INTO player_fact ("
            "   id,"
            "   original_id,"
            "   team_id,"
            "   player_id,"
            "   league_id,"
            "   age_range_id,"
            "   infractions_avg_range_id,"
            "   goals_frequency_range_id,"
            "   assists_frequency_range_id,"
            "   position_id,"
            "   yellow_cards,"
            "   red_cards,"
            "   goals,"
            "   assists,"
            "   goals_per_90_min,"
            "   assists_per_90_min,"
            "   shots,"
            "   goals_per_shot,"
            "   matches_played,"
            "   starting_matches,"
            "   minutes_played,"
            "   completed_passes,"
            "   overall_score,"
            "   completed_passes_percentage,"
            "   goals_per_match,"
            "   market_value,"
            "   creation_date,"
            "   assists_per_match"
            ") VALUES ("
            "   %(id)s,"
            "   %(original_id)s,"
            "   (SELECT id FROM team WHERE source_id=%(team_source_id)s),"
            "   (SELECT id FROM player_profile WHERE source_id=%(player_source_id)s),"
            "   (SELECT id FROM league WHERE source_id=%(league_source_id)s),"
            "   (SELECT id FROM age_range WHERE start_value <= %(age)s::int AND end_value >= %(age)s::int),"
            "   (SELECT id FROM infractions_by_match_average_range WHERE start_value <= %(infractions_by_match)s::int AND end_value >= %(infractions_by_match)s::int LIMIT 1),"
            "   (SELECT id FROM goals_frequency_range WHERE start_value <= %(goals_by_match)s::int AND end_value >= %(goals_by_match)s::int LIMIT 1),"
            "   (SELECT id FROM assists_frequency_range WHERE start_value <= %(assists_per_match)s::int AND end_value >= %(assists_per_match)s::int LIMIT 1),"
            "   (SELECT id FROM position WHERE name=%(position_name)s),"
            "   %(yellow_cards)s,"
            "   %(red_cards)s,"
            "   %(goals)s,"
            "   %(assists)s,"
            "   %(goals_per_90_min)s,"
            "   %(assists_per_90_min)s,"
            "   %(shots)s,"
            "   %(goals_per_shot)s,"
            "   %(matches_played)s,"
            "   %(starting_matches)s,"
            "   %(minutes_played)s,"
            "   %(completed_passes)s,"
            "   %(overall_score)s,"
            "   %(completed_passes_percentage)s,"
            "   %(goals_per_match)s,"
            "   %(market_value)s,"
            "   %(created_date)s,"
            "   %(assists_per_match)s"
            ")",
            {
                "id": uuid.uuid4(),
                "original_id": row["id"],
                "team_source_id": row["Club_x_id"],
                "player_source_id": row["id"],
                "league_source_id": row["League_id"],
                "age": row["Age"],
                "infractions_by_match": row["Infractions by match"],
                "goals_by_match": row["Goals by match"],
                "assists_per_match": row["Assists by match"],
                "position_name": row["Pos"].split(",")[0],
                "yellow_cards": row["CrdY"],
                "red_cards": row["CrdR"],
                "goals": row["Gls"],
                "assists": row["Ast"],
                "goals_per_90_min": row["Gls90"],
                "assists_per_90_min": row["Ast90"],
                "shots": row["SoT"],
                "goals_per_shot": row["G/SoT"],
                "matches_played": row["MP"],
                "starting_matches": row["Starts"],
                "minutes_played": row["Min"],
                "completed_passes": row["Passes Attempted"],
                "overall_score": row["Overall point"],
                "completed_passes_percentage": row["Cmp%"],
                "goals_per_match": row["Goals by match"],
                "market_value": row["Market value"],
                "created_date": BATCH_DATE
            }
        )
    connection.commit()


frequency_dimension_calc_class = FrequencyDimensionCalc()

data_frame = clean_dataframe(data_frame)

# adicionado novas colunas
data_frame = add_column_infractions(data_frame)
data_frame = add_column_infractions_by_match(data_frame)
data_frame = add_overall_point_column(data_frame)
data_frame = add_goals_by_match(data_frame)
data_frame = add_assists_by_match(data_frame)

# salvando dimensões
save_teams(data_frame)
save_leagues(data_frame)
save_positions(data_frame)
save_infractions_by_match_average_ranges()
save_ages_range()
save_passes_range()
frequency_dimension_calc_class.compute_goals(data_frame)
frequency_dimension_calc_class.compute_assists(data_frame)
frequency_dimension_calc_class.update_all_players()

save_players_profiles(data_frame)
save_players(data_frame)

print("PostgreSQL Table %s has been created successfully." % soccer_table)
connection.close()
