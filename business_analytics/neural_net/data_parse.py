import pandas as pd
import numpy as np

def parse(data_filepath):
    data = pd.read_csv(data_filepath)
    cols_to_drop = ['Season', 'Game_ID', 'Away_Team', 'Home_Team']
    data = data.drop(columns=cols_to_drop)
    data.is_christmas = data.is_christmas.astype(int)
    data.is_weekend = data.is_weekend.astype(int)
    data.First_Five_Games = data.First_Five_Games.astype(int)
    data.is_opening_day = data.is_opening_day.astype(int)
    data.to_csv(data_filepath, index=False)

def main():
    parse('new_train.csv')
    parse('new_test.csv')

if __name__ == '__main__':
    main()


