from datetime import datetime
import pandas as pd
import numpy as np
import lib_dict

def update_game_data():
    data_1617 = pd.read_csv('2016-17_teamBoxScore.csv')
    data_1718 = pd.read_csv('2017-18_teamBoxScore.csv')
    game_data = pd.read_csv('game_data.csv')
    official_data = pd.concat([data_1617, data_1718])

    ### Format Dates ###
    game_data['Game_Date'] = [datetime.strptime(d, '%m/%d/%Y') for d in game_data['Game_Date']]
    official_data['gmDate'] = [datetime.strptime(d, '%Y-%m-%d') for d in official_data['gmDate']]

    ### Update Game Codes ###
    official_data = official_data.replace(lib_dict.team_dict)

    ### Update Game Data ###
    for row_index, row in game_data.iterrows():

        team_name = row['Team']
        game_date = row['Game_Date']

        official_row  = official_data.loc[(official_data['gmDate'] == game_date) & \
                (official_data['teamAbbr'] == team_name)]

        game_data.loc[row_index, 'Pace'] = int(official_row['pace'])
        game_data.loc[row_index, 'EffFG'] = float(official_row['teamEFG%'])
        game_data.loc[row_index, 'FGA'] = int(official_row['teamFGA'])
        game_data.loc[row_index, 'FTA'] = int(official_row['teamFTA'])
        game_data.loc[row_index, 'Game_Time'] = str(official_row['gmTime'].item())
        game_data.loc[row_index, 'Fouls'] = int(official_row['teamPF'])

        q1_points = int(official_row['teamPTS1'])
        q2_points = int(official_row['teamPTS2'])
        q3_points = int(official_row['teamPTS3'])
        q4_points = int(official_row['teamPTS4'])
        ot1_points = int(official_row['teamPTS5'])
        ot2_points = int(official_row['teamPTS6'])
        ot3_points = int(official_row['teamPTS7'])
        ot4_points = int(official_row['teamPTS8'])

        game_data.loc[row_index, 'HT_Score'] = q1_points + q2_points

        ### Update Nan Values ###
        if np.isnan(row['Team_Minutes']):
            minutes = int(official_row['teamMin'])
            game_data.loc[row_index, 'Team_Minutes'] = minutes
            total_score = q1_points + q2_points + q3_points + q4_points + ot1_points + \
                    ot2_points + ot3_points + ot4_points
            q4_score = q1_points + q2_points + q3_points
            game_data.loc[row_index, 'Final_Score'] = total_score
            game_data.loc[row_index, 'Qtr_4_Score'] = q4_score

        game_data.to_csv('game_data_new.csv')
    return data

def update_data(data_filepath, game_data):
    data = pd.read_csv(data_filepath)
    for index, row in data.iterrows():
        home_team = row.Home_Team
        away_team = row.Away_Team
        game_id = row.Game_ID
        home_data = game_data.loc[(game_data.Team == home_team) & \
                (game_data.Game_ID == game_id)]
        away_data = game_data.loc[(game_data.Team == away_team) & \
                (game_data.Game_ID == game_id)]
        both_data = game_data.loc[game_data.Game_ID == game_id]


def main():
    data = update_game_data()
    #update_data('new_train.csv', data)
    #update_data('new_test.csv', data)

if __name__ == '__main__':
    main()



