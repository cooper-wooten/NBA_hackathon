import pandas as pd
import numpy as np

def get_data():
    return pd.read_csv('awards_data.csv')

def update_data(data_filepath, awards_data):
    data = pd.read_csv(data_filepath)
    awards = ['MVP', 'SMA', 'ROY', 'MIP', 'DPOY', 'All_NBA']
    for index, row in data.iterrows():
        home_team = row.Home_Team
        away_team = row.Away_Team
        season = row.Season

        for award in awards:
            award_rows = awards_data.loc[((awards_data.Team == home_team) | \
                    (awards_data.Team == away_team)) & \
                    (awards_data.Season == season) & (awards_data.Award_type == award)]
            points = sum(award_rows.Points)
            data.loc[index, award + '_points'] = points
    data.to_csv(data_filepath, index=False)

def main():
    awards_data = get_data()
    update_data('new_test.csv', awards_data)
    update_data('new_train.csv', awards_data)

if __name__ == '__main__':
    main()

