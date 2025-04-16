from dotenv import load_dotenv
import os
import json
import sqlite3
import pandas as pd
import gc

def format_name(name):
    return ".".join(part[0].upper() for part in name.split()) + "."

# Loads env variables
load_dotenv(verbose=False)
kaggle_path = os.path.expanduser("~/.kaggle")
os.makedirs(kaggle_path, exist_ok=True)

kaggle_json = {
    "username": os.getenv("KAGGLE_USERNAME"),
    "key": os.getenv("KAGGLE_KEY")
}

with open(os.path.join(kaggle_path, "kaggle.json"), "w") as f:
    json.dump(kaggle_json, f)

os.chmod(os.path.join(kaggle_path, "kaggle.json"), 0o600)

from kaggle.api.kaggle_api_extended import KaggleApi

# Files and paths
kaggle_resource = 'guillemservera/tennis'
origin_db_file_name = 'database.sqlite'
destination_db_file_name = 'tennisdb2.sqlite'

script_dir = os.getcwd()
path = os.path.join(script_dir, "app", "data")
origin_database_path = os.path.join(path, origin_db_file_name)
destination_database_path = os.path.join(path, destination_db_file_name)

# Inits api
api = KaggleApi()
api.authenticate()

# Downloads dataset
api.dataset_download_files(
   dataset=kaggle_resource,
   path=path,
   unzip=True,
   quiet=True
)

# Connects and converts into dataframes
try:
   conn = sqlite3.connect(origin_database_path)
   cursor = conn.cursor()
except sqlite3.Error as err:
   print(f"An error ocurred during connection to database {origin_db_file_name}: {err}")
   exit()
   
try:
   conn_cleaned = sqlite3.connect(destination_database_path)
except sqlite3.Error as err:
   print(f"An error occurred during connection to database {destination_db_file_name}: {err}")
   exit()
    
# Loads and processes players
try:
   query = "SELECT * FROM players;"
   players_df = pd.read_sql_query(query, conn)

   # Clean players
   players_df = players_df.replace('Unknown', 'unknown')
   players_df = players_df[~(players_df['name_last'].isnull() |
      (players_df['name_last'].str.strip() == '') |
      (players_df['name_last'].str.strip() == '?') |
      (players_df['name_last'].str.strip() == 'unknown'))]

   string_columns = ['name_first', 'name_last', 'ioc', 'wikidata_id', 'height', 'hand']
   for column in string_columns:
      players_df[column] = players_df[column].fillna('unknown')
      players_df[column] = players_df[column].apply(lambda x: 'unknown' if isinstance(x, str) and (x.strip() == '' or x.strip() == '?') else x)
      
   players_df.loc[players_df['hand'] == 'U', 'hand'] = 'unknown'
   players_df['dob'] = players_df['dob'].fillna(18000101).astype(int).astype(str)

   mask = players_df['height'] != 'unknown'
   players_df.loc[mask, 'height'] = players_df.loc[mask, 'height'].astype(float).astype(int).astype(str)
   players_df['player_id'] = players_df['player_id'].astype(str)
   players_df['dob'] = players_df['dob'].apply(lambda x: x[:4] + '0101' if x.endswith('0000') else x)
   players_df['dob'] = pd.to_datetime(players_df['dob'], format='%Y%m%d').dt.date

   players_df['capitals_name_first'] = players_df['name_first'].apply(format_name)
   mask = players_df['name_first'] == 'unknown'
   players_df['fullname'] = players_df['name_last'].str.strip() + ' ' + players_df['capitals_name_first'].str.strip()
   players_df.loc[mask, 'fullname'] = players_df.loc[mask, 'name_last'].str.strip()
   players_df = players_df.drop(columns=['capitals_name_first'])
   players_df['weight'] = 'unknown'
   players_df['instagram'] = 'unknown'
   players_df['facebook'] = 'unknown'
   players_df['x_twitter'] = 'unknown'
   players_df['pro_since'] = 'unknown'

   columns_dict = {
      'dob': 'birth_date',
      'ioc': 'country',
   }
   players_df.rename(columns=columns_dict, inplace=True)

   duplicated_rows = players_df.duplicated(subset=['name_last', 'name_first', 'birth_date']).sum()
   players_df.drop_duplicates(subset=['name_last', 'name_first', 'birth_date'], inplace=True)

   # Writes database
   players_df.to_sql('players', conn_cleaned, if_exists='replace', index=False)
      
except sqlite3.Error as err:
   print(f"An error occurred during players processing: {err}")
finally:
   del players_df
   gc.collect()

# Loads and processes rankings
try:
   query = "SELECT * FROM rankings;"
   rankings_df = pd.read_sql_query(query, conn)

   # Cleans rankings
   rankings_df['points'] = rankings_df['points'].fillna('unknown')
   rankings_df['points'] = rankings_df['points'].apply(
      lambda x: str(int(x)) if x != 'unknown' else x
   )

   rankings_df['player_id'] = rankings_df['player'].astype(str)
   rankings_df['rank'] = rankings_df['rank'].astype(str)
   rankings_df['ranking_date'] = pd.to_datetime(rankings_df['ranking_date'], format='%Y%m%d').dt.date

   rankings_df.drop(columns=['player'], inplace=True)
   
   # Writes database
   rankings_df.to_sql('rankings', conn_cleaned, if_exists='replace', index=False)
   
except sqlite3.Error as err:
   print(f"An error occurred during rankings processing: {err}")
finally:
   del rankings_df
   gc.collect()
   

# Loads and processes matches
try:
   invalid_levels = ['C', 'S', 'E', 'J', 'T', '15', '25']
   invalid_levels_str = ', '.join(f"'{level}'" for level in invalid_levels)
   
   query = f"""
   SELECT * FROM matches
   WHERE winner1_id IS NULL
   AND winner2_id IS NULL
   AND loser1_id IS NULL
   AND loser2_id IS NULL
   AND tourney_level NOT IN ({invalid_levels_str});
  """
   matches_df = pd.read_sql_query(query, conn)

   # Cleans matches
   levels = ['G', 'M', 'A', 'C', 'S', 'F', 'D', 'E', 'J', 'T']
   mask = (~matches_df['tourney_level'].isin(levels)) & (matches_df['tourney_level'].str.len() == 8)
   matches_df.loc[mask, matches_df.columns[1:-1]] = matches_df.loc[mask, matches_df.columns[0:-2]].values
   matches_df.loc[mask, 'tourney_id'] = '0'

   other_levels = [x for x in matches_df['tourney_level'].unique() if x not in levels]
   matches_df = matches_df[~matches_df['tourney_level'].isin(other_levels)]
   drop_levels = ['C', 'S', 'E', 'J', '15', '25']
   matches_df = matches_df[~matches_df['tourney_level'].isin(drop_levels)]

   matches_df = matches_df[matches_df[['winner1_id', 'winner2_id', 'loser1_id', 'loser2_id']].isnull().all(axis=1)]
   drop_columns = [
      'tourney_id',
      'match_num',
      'draw_size',
      'winner_name',
      'winner_hand',
      'winner_ht',
      'winner_ioc',
      'winner_age',
      'loser_name',
      'loser_hand',
      'loser_ht',
      'loser_ioc',
      'loser_age',
      'winner_rank',
      'winner_rank_points',
      'loser_rank',
      'loser_rank_points',
      'winner1_name',
      'winner1_hand',
      'winner1_ht',
      'winner1_ioc',
      'winner1_age',
      'winner2_name',
      'winner2_hand',
      'winner2_ht',
      'winner2_ioc',
      'winner2_age',
      'loser1_name',
      'loser1_hand',
      'loser1_ht',
      'loser1_ioc',
      'loser1_age',
      'loser2_name',
      'loser2_hand',
      'loser2_ht',
      'loser2_ioc',
      'loser2_age',
      'winner1_rank',
      'winner1_rank_points',
      'winner2_rank',
      'winner2_rank_points',
      'loser1_rank',
      'loser1_rank_points',
      'loser2_rank',
      'loser2_rank_points',
      'winner1_id',
      'winner2_id',
      'loser1_id',
      'loser2_id',
      'winner_seed',
      'winner_entry',
      'loser_seed',
      'loser_entry',
      'minutes'
   ]
   matches_df = matches_df.drop(columns=drop_columns)

   duplicated_rows = matches_df.duplicated().sum()
   matches_df.drop_duplicates(inplace=True)
   matches_df = matches_df.replace('Unknown', 'unknown')
   matches_df = matches_df.replace('None', 'unknown')
   matches_df = matches_df.replace('?', 'unknown')
   string_columns = [
      'surface',
      'tourney_level',
      'score'
   ]
   for column in string_columns:
      matches_df[column] = matches_df[column].fillna('unknown')
      
   numerical_columns = [
      'w_ace',
      'w_df',
      'w_svpt',
      'w_1stIn',
      'w_1stWon',
      'w_2ndWon',
      'w_SvGms',
      'w_bpSaved',
      'w_bpFaced',
      'l_ace',
      'l_df',
      'l_svpt',
      'l_1stIn',
      'l_1stWon',
      'l_2ndWon',
      'l_SvGms',
      'l_bpSaved',
      'l_bpFaced'
   ]
   for column in numerical_columns:
      matches_df[column] = matches_df[column].fillna(0)

   for column in numerical_columns:
      matches_df[column] = matches_df[column].astype(int).astype(str)

   matches_df['winner_id'] = matches_df['winner_id'].astype(int).astype(str)
   matches_df['loser_id'] = matches_df['loser_id'].astype(int).astype(str)
   matches_df['tourney_date_aux'] = pd.to_datetime(matches_df['tourney_date'].astype(int).astype(str), format='%Y%m%d')
   matches_df['tourney_date'] = pd.to_datetime(matches_df['tourney_date'], format='%Y%m%d').dt.date
   matches_df['year'] = matches_df['tourney_date_aux'].dt.year.astype(str)
   matches_df['court'] = 'unknown'
   matches_df.rename(columns={
      'w_ace': 'w_aces',
      'l_ace': 'l_aces'
   }, inplace=True)
   levels_dict = {
      'A': 'Other ATP',
      'G': 'Grand Slam',
      'D': 'Davis Cup',
      'M': 'Masters 1000',
      'F': 'ATP Finals'
   }
   matches_df['tourney_level'] = matches_df['tourney_level'].astype(str).str.strip()
   matches_df['tourney_level'] = matches_df['tourney_level'].map(levels_dict)
   mask = (matches_df['tourney_level'] == 'Other ATP') & (matches_df['tourney_name'].str.contains('Olympics', na=False))
   matches_df.loc[mask, 'tourney_level'] = 'Olympics'
   mapping_dict = {
      'R128': '1st Round',
      'R64': '2nd Round',
      'R32': '3rd Round',
      'R16': '4th Round',
      'QF': 'Quarterfinals',
      'SF': 'Semifinals',
      'F': 'The Final',
      'RR': 'Round Robin',
      'BR': 'Bronze Match',
      'Q1': 'Qualification Round 1',
      'Q2': 'Qualification Round 2',
      'Q3': 'Qualification Round 3',
      'ER': 'Early Round',
      'Q4': 'Qualification Round 4',
      'CR': 'Consolation Round',
      'PR': 'Preliminary Round'
   }
   matches_df['round'] = matches_df['round'].astype(str).str.strip()
   matches_df['round'] = matches_df['round'].map(mapping_dict)
   matches_df = matches_df[matches_df['tourney_name'] != 'Doha Aus Open Qualies']
   names = ['Australian Chps.', 'Australian Open-2']
   matches_df.loc[
      (matches_df['tourney_level'] == 'Grand Slam') & (matches_df['tourney_name'].isin(names)),
      'tourney_name'
   ] = 'Australian Open'

   matches_df.loc[
      (matches_df['tourney_level'] == 'Grand Slam') & (matches_df['tourney_name'] == 'Us Open'),
      'tourney_name'
   ] = 'US Open'
   matches_df.loc[
      (matches_df['tourney_level'] == 'Masters 1000') & (matches_df['tourney_name'] == 'Indian Wells'),
      'tourney_name'
   ] = 'Indian Wells Masters'

   matches_df.loc[
      (matches_df['tourney_level'] == 'Masters 1000') & (matches_df['tourney_name'] == 'Cincinnati'),
      'tourney_name'
   ] = 'Cincinnati Masters'

   matches_df.loc[
      (matches_df['tourney_level'] == 'Masters 1000') & (matches_df['tourney_name'] == 'Rome'),
      'tourney_name'
   ] = 'Rome Masters'

   matches_df.loc[
      (matches_df['tourney_level'] == 'Masters 1000') & (matches_df['tourney_name'] == 'Key Biscayne'),
      'tourney_name'
   ] = 'Miami Masters'

   names = ['Montreal / Toronto', 'Toronto']
   matches_df.loc[
      (matches_df['tourney_level'] == 'Masters 1000') & (matches_df['tourney_name'].isin(names)),
      'tourney_name'
   ] = 'Canada Masters'
   tourneys_to_drop = ['Masters', 'Stockholm Masters', 'Boca West', 'Masters Dec', 'Delray Beach']
   matches_df = matches_df[~matches_df['tourney_name'].isin(tourneys_to_drop)]

   # Writes database 
   matches_df.to_sql('matches', conn_cleaned, if_exists='replace', index=False)
except sqlite3.Error as err:
   print(f"An error occurred during matches processing: {err}")
finally:
   print("matches end")
   del matches_df
   gc.collect()
   
try:
   if 'conn' in locals():
      conn.close()
   if 'conn_cleaned' in locals():
      conn_cleaned.close()
except sqlite3.Error as e:
   print(f"Error closing connections: {e}")
