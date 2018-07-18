import pandas as pd
import numpy as np
import lib_dict

def parse():
    shot_data = pd.read_excel('shot_type_data.xlsx')
    shot_data = shot_data.replace(lib_dict.teamname_dict)
    return shot_data

def calculate_percent(percent_shots, percent_made):
    return percent_shots*percent_made/100

def get_shot_values(data):
    shot_types = ['jumpshots', 'layups', 'dunks', 'tipins']
    for index, row in data.iterrows():
        for shot in shot_types:
            team_shot = row[shot]
            team_made = row[shot+'%']
            opp_shot = row['opp_'+shot]
            opp_made = row['opp_'+shot+'%']
            col_name = shot + '_value'
            oppcol_name = 'opp_' + shot + '_value'
            data.loc[index, col_name] = calculate_percent(team_shot, team_made)
            data.loc[index, oppcol_name] = calculate_percent(opp_shot, opp_made)
    return data

def update_data(data_filepath, shot_data):
    data = pd.read_csv(data_filepath)
    for index, row in data.iterrows():
        home_team = row.Home_Team
        away_team = row.Away_Team
        season = row.Season
        home_data = shot_data.loc[(shot_data.Team == home_team) & \
                (shot_data.Season == season)]
        away_data = shot_data.loc[(shot_data.Team == away_team) & \
                (shot_data.Season == season)]
        shot_types = ['jumpshots', 'layups', 'dunks', 'tipins']
        for shot in shot_types:
            home_name = shot + '_value'
            away_name = 'opp_' + shot + '_value'
            value = np.mean([home_data[home_name].values, home_data[away_name].values, \
                    away_data[home_name].values, away_data[away_name].values])
            data.loc[index, shot + '_made'] = value
    data.to_csv(data_filepath)

def main():
    shot_data = parse()
    data = get_shot_values(shot_data)
    update_data('new_test.csv', data)
    update_data('new_train.csv', data)

if __name__ == '__main__':
    main()

