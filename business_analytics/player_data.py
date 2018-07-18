from datetime import datetime
import pandas as pd
import numpy as np
import lib_dict

def parse():
    data = pd.read_csv('player_data.csv')
   ### Replace Codes ###
    data = data.replace(lib_dict.allstar_dict)
    data = data.replace(lib_dict.active_dict)
    data = data[(data.ASG_Team == 1) & (data.Active_Status == 1)]
    return data

def update_nan(data):
    data_1617 = pd.read_csv('2016-17_playerBoxScore.csv')
    data_1718 = pd.read_csv('2017-18_playerBoxScore.csv')
    official_data = pd.concat([data_1617, data_1718])
    ### Format Dates ###
    data['Game_Date'] = [datetime.strptime(d, '%m/%d/%Y') for d in data['Game_Date']]
    official_data['gmDate'] = [datetime.strptime(d, '%Y-%m-%d') for d in official_data['gmDate']]

    for row_index, row in data.iterrows():
        names = row['Name']
        game_date = row['Game_Date']

        official_row = official_data.loc[(official_data['gmDate'] == game_date) & \
                (official_data.playDispNm == names)]

        if not official_row.empty and np.isnan(row['Minutes']):
            data.loc[row_index, 'Minutes'] = int(official_row['playMin'])
            data.loc[row_index, 'Points'] = int(official_row['playPTS'])
            data.loc[row_index, 'Defensive_Rebounds'] = int(official_row['playDRB'])
            data.loc[row_index, 'Offensive_Rebounds'] = int(official_row['playORB'])
            data.loc[row_index, 'Assists'] = int(official_row['playAST'])
            data.loc[row_index, 'Steals'] = int(official_row['playSTL'])
            data.loc[row_index, 'Blocks'] = int(official_row['playBLK'])
            data.loc[row_index, 'Turnovers'] = int(official_row['playTO'])
            data.loc[row_index, 'Field_Goals'] = int(official_row['playFGM'])
            data.loc[row_index, 'Field_Goals_Attempted'] = int(official_row['playFGA'])
            data.loc[row_index, 'Three_Pointers'] = int(official_row['play3PM'])
            data.loc[row_index, 'Three_Pointers_Attempted'] = int(official_row['play3PA'])
            data.loc[row_index, 'Free_Throws'] = int(official_row['playFTM'])
            data.loc[row_index, 'Free_Throws_Attempted'] = int(official_row['playFTA'])
            data.loc[row_index, 'Personal_Fouls'] = int(official_row['playPF'])

    data = data[(~data.Minutes.isnull()) & (data.Minutes > 0)]
    data.to_csv('player_data_new.csv')
    return data

def update_data(data_filepath, player_data):
    data = pd.read_csv(data_filepath)
    for index, row in data.iterrows():
        game_id = row['Game_ID']
        player_rows = player_data.loc[player_data.Game_ID == game_id]
        allstar_points = sum(player_rows.Points)
        data.loc[index, 'All_Star_Points'] = allstar_points
        num_allstars = player_rows.shape[0]
        if num_allstars > 0:
            data.loc[index, 'Avg_Allstar_Points'] = allstar_points/num_allstars
            per = 0
            for player_index, player_row in player_rows.iterrows():
                minutes = player_row['Minutes']
                fg = player_row['Field_Goals']
                steals = player_row['Steals']
                three_pt = player_row['Three_Pointers']
                ft = player_row['Free_Throws']
                blocks = player_row['Blocks']
                offreb = player_row['Offensive_Rebounds']
                assists = player_row['Assists']
                defreb = player_row['Defensive_Rebounds']
                pf = player_row['Personal_Fouls']
                fta = player_row['Free_Throws_Attempted']
                fga = player_row['Field_Goals_Attempted']
                to = player_row['Turnovers']
                per += (1/minutes)*(85.91*fg + 53.897*steals + 51.757*three_pt + \
                        46.845*ft + 39.19*offreb + 34.677*assists + 14.707*defreb - \
                        17.174*pf - 20.091*(fta-ft) - 39.19*(fga-fg) - 53.897*to)
            per_per = per/num_allstars
            data.loc[index, 'Total_PER'] = per
            data.loc[index, 'Avg_PER'] = per_per
        else:
            data.loc[index, 'Avg_Allstar_Points'] = 0
            data.loc[index, 'Total_PER'] = 0
            data.loc[index, 'Avg_PER'] = 0

        data.to_csv(data_filepath, index=False)

def main():
    data = parse()
    player_data = update_nan(data)
    update_data('new_train.csv', player_data)
    update_data('new_test.csv', player_data)

if __name__ == '__main__':
    main()

