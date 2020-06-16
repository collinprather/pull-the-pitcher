# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_data_acquisition.ipynb (unless otherwise specified).

__all__ = ['query_statcast', 'query_db']

# Internal Cell
from pybaseball import statcast
import pandas as pd
from fastscript import *
import sqlite3

# Cell


@call_parse
def query_statcast(
    start_dt: Param(help="Beginning date to pull data from", type=str) = None,
    end_dt: Param(help="End date to pull data from", type=str) = None,
    team: Param(help="Abbreviation for team of interest", type=str) = None,
    verbose: Param(
        help="Whether or not to print verbose updates", type=bool_arg
    ) = True,
    output_type: Param(help="What format to save data in", type=str) = "db",
    overwrite: Param(
        help="Whether or not to overwrite the db table if it already exists",
        type=bool_arg,
    ) = True,
    output_path: Param(
        help="path to location that data should be saved", type=str
    ) = ".",
):
    """
    Callable from the command-line or in Python. Pulls pitch-level MLB data from [statcast](https://baseballsavant.mlb.com/statcast_search).
    Saves as either a sqlite db file, or csv.

    inputs:
        - `start_dt`: `str`, Beginning date to pull data from = None
        - `end_dt`: `str`, End date to pull data from = None
        - `team`: `str`, abbreviation for team of interest = None
        - `verbose`: `bool`, Whether or not to print verbose updates
        - `output_type`: `str`, What format to save data in (must be one of {'db', 'csv'}) = 'db'
        - `overwrite`: `bool`, Whether or not to overwrite the db table if it already exists = True
        - `output_path`: `str`, Path to the location that the data should be saved at = '.'

    outputs:
        - None
    """
    # checking for correct output type
    if output_type not in ("db", "csv"):
        raise ValueError("output_type must be one of {'db', 'csv'}")

    # pulling data from statcast
    data = statcast(start_dt, end_dt, team, verbose)

    if output_type == "db":
        # creating db
        conn = sqlite3.connect(f"{output_path}/statcast_pitches.db")
        if overwrite:
            conn.execute(f"DROP TABLE IF EXISTS statcast_{start_dt[:4]}")
        data.to_sql(f"statcast_{start_dt[:4]}", conn)
        conn.close()

    else:
        # saving to csv
        data.to_csv(f"{output_path}/statcast_{start_dt[:4]}.csv", index=False)

    return None


# Cell


def query_db(
    db_path: str = "../data/raw/statcast_pitches.db",
    year: str = "2019",
    columns: str = "*",
    limit: int = None,
    verbose: bool = True,
):
    """
    Queries a sqlite db file. Assumes that it's been created by `query_statcast`.
    Only queries for a single year at a time.

    intputs:
        - `db_path`: `str`, path that db file is located at
        - `year`: `str`, year of data to query
        - `columns`: `str`, which columns from the [statcast data](https://baseballsavant.mlb.com/csv-docs) to include in table
        - `limit`: `int`, the maximum number of rows to retrieve ([postgresql documentation](https://www.postgresql.org/docs/8.1/queries-limit.html))
        - `verbose`: `bool`, Whether or not to print verbose updates

    output:
        - `df`: `pd.DataFrame`, DataFrame populated with data queried from database
    """
    if verbose:
        print(f"querying db at {db_path} now.")
    conn = sqlite3.connect(db_path)
    query = f"""select {columns}
                from statcast_{year}"""
    if limit:
        query += f" limit {round(limit)}"

    # making sure year is in db
    cursor = conn.execute(f"select name from sqlite_master where type='table' and name='statcast_{year}'")
    if cursor.fetchone():
        df = pd.read_sql_query(query, conn)
    else:
        df = pd.DataFrame()
    conn.close()
    return df
