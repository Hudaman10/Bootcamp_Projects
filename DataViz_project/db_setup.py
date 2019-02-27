#Dependencies
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
import pymysql
pymysql.install_as_MySQLdb()


###Import Datasets
#Player Data
player_file = "./Data/Players.csv"
player_df = pd.read_csv(player_file)

#College State Data
college_file = "./Data/hd2017.csv"
college_df = pd.read_csv(college_file, encoding='latin-1')

#Dataset with state names and their abreviations
state_file = "./Data/state_abv.csv"
state_df = pd.read_csv(state_file)


###Clean Datasets

#Dropping unnecessary columns and renaming mispelled columns from player_df
clean_player_df = player_df[['Player', 'collage', 'birth_state']].copy()
clean_player_df = clean_player_df.rename(columns={'Player':'player','collage':'college'})

#Dropping unnecessary columns and renaming  columns from college_df
clean_college_df = college_df[['INSTNM', 'STABBR']].copy()
clean_college_df = clean_college_df.rename(columns={'INSTNM': 'college', 'STABBR': 'Abbreviation'})

#Merging state and college dataframes and dropping abbreviation column
clean_college_df = clean_college_df.merge(state_df, on='Abbreviation')
clean_college_df = clean_college_df.drop(columns='Abbreviation')

#Merging college and player dataframes
clean_player_df = clean_player_df.merge(clean_college_df, on="college")
clean_player_df = clean_player_df.rename(columns={"State":"college_state"})
clean_player_df = clean_player_df.merge(state_df, how="left", left_on="birth_state", right_on="State")

#Dropping NaNs and and State and Abbreviation columns
clean_player_df = clean_player_df.dropna()
clean_player_df = clean_player_df.drop(columns=['State', 'Abbreviation'])


###Saving to a csv
clean_player_df.to_csv('nba_complete.csv')

##############################################################################

###Creating database connection  
connection_string = "root:Mars@localhost/ncaa_db"
engine = create_engine(f'mysql://{connection_string}')

#Load data into SQL database
clean_player_df.to_sql(name='ncaa_info', con=engine, if_exists='append', index=False)
