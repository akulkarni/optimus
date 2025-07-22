import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, Boolean, MetaData

# --- CONFIGURATION ---
CONNECTION_STRING = "postgres://tsdbadmin:mh05b2wc56tpbge6@dame8y37oj.ye4xypn0ge.tsdb.cloud.timescale.com:35540/tsdb?sslmode=require"
CSV_FILE = "whoop_workouts.csv"  # Change this to your CSV file path
TABLE_NAME = "whoop_workouts"

# --- READ CSV ---
df = pd.read_csv(CSV_FILE)

# --- DATA CLEANING (convert empty strings to None) ---
df = df.where(pd.notnull(df), None)

# --- SETUP SQLALCHEMY ENGINE ---
engine = create_engine(CONNECTION_STRING)
metadata = MetaData()

# --- DEFINE TABLE ---
whoop_workouts = Table(
    TABLE_NAME, metadata,
    Column('cycle_start_time', String),
    Column('cycle_end_time', String),
    Column('cycle_timezone', String),
    Column('workout_start_time', String),
    Column('workout_end_time', String),
    Column('duration_min', Float),
    Column('activity_name', String),
    Column('activity_strain', Float),
    Column('energy_burned_cal', Float),
    Column('max_hr_bpm', Integer),
    Column('average_hr_bpm', Integer),
    Column('hr_zone_1_pct', Float),
    Column('hr_zone_2_pct', Float),
    Column('hr_zone_3_pct', Float),
    Column('hr_zone_4_pct', Float),
    Column('hr_zone_5_pct', Float),
    Column('gps_enabled', Boolean),
    Column('distance_meters', Float),
    Column('altitude_gain_meters', Float),
    Column('altitude_change_meters', Float),
)

# --- CREATE TABLE IF NOT EXISTS ---
metadata.create_all(engine, checkfirst=True)

# --- RENAME COLUMNS TO MATCH DB ---
df.columns = [
    'cycle_start_time', 'cycle_end_time', 'cycle_timezone', 'workout_start_time', 'workout_end_time',
    'duration_min', 'activity_name', 'activity_strain', 'energy_burned_cal', 'max_hr_bpm', 'average_hr_bpm',
    'hr_zone_1_pct', 'hr_zone_2_pct', 'hr_zone_3_pct', 'hr_zone_4_pct', 'hr_zone_5_pct',
    'gps_enabled', 'distance_meters', 'altitude_gain_meters', 'altitude_change_meters'
]

# --- CONVERT BOOLEAN COLUMN ---
df['gps_enabled'] = df['gps_enabled'].map({'true': True, 'false': False, True: True, False: False, None: None})

# --- INSERT DATA ---
df.to_sql(TABLE_NAME, engine, if_exists='append', index=False, method='multi')

print(f"Loaded {len(df)} rows into {TABLE_NAME}.")
