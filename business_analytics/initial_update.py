import datetime
import numpy as np
import pandas as pd

def update_data(option='train'):

    if option == 'train':
        data = pd.read_csv('new_train.csv')
    else:
        data = pd.read_csv('test_set.csv')

    game_data = pd.read_csv('game_data_new.csv')
    player_data = pd.read_csv('player_data_new.csv')

    data = data.drop(columns=['All_Stars_Away', 'All_Stars_Home', 'All_Stars_Total',\
            'International_Home', 'International_Away']) # don't use for test set

# is_weekend column
    data['Game_Date'] = [datetime.datetime.strptime(d, '%m/%d/%Y') for d in data['Game_Date']]
    weekends = [5,6]
    data['weekday'] = [d.weekday() for d in data.Game_Date]
    data.loc[data.weekday.isin(weekends), 'is_weekend'] = True
    data.loc[~data.weekday.isin(weekends), 'is_weekend'] = False

# is_christmas column
    christmas = (12,25)
    data['month'] = [d.month for d in data['Game_Date']]
    data['day'] = [d.day for d in data['Game_Date']]
    data.loc[(data.month == christmas[0]) & (data.day == christmas[1]), 'is_christmas'] = True
    data.loc[(data.month != christmas[0]) | (data.day != christmas[1]), 'is_christmas'] = False


    columns_to_drop = ['weekday', 'month', 'day']
    data = data.drop(columns=columns_to_drop)

    for row_index, row in data.iterrows():
        game_id = row['Game_ID']
        game_rows = game_data.loc[(game_data['Game_ID'] == game_id)]
        player_rows = player_data.loc[(player_data['Game_ID'] == game_id)]

        # Total Shots Attempted
        data.loc[row_index, 'Total_FGA'] = sum(game_rows.FGA.values)
        data.loc[row_index, 'Total_FTA'] = sum(game_rows.FTA.values)

        # Score Differences
        t1_ht_score = game_rows.HT_Score.values[0]
        t2_ht_score = game_rows.HT_Score.values[1]
        data.loc[row_index, 'HT_Diff'] = abs(t1_ht_score-t2_ht_score)
        t1_q4_score = game_rows.Qtr_4_Score.values[0]
        t2_q4_score = game_rows.Qtr_4_Score.values[1]
        data.loc[row_index, 'Q4_Diff'] = abs(t1_q4_score-t2_q4_score)
        t1_final_score = game_rows.Final_Score.values[0]
        t2_final_score = game_rows.Final_Score.values[1]
        data.loc[row_index, 'Final_Diff'] = abs(t1_final_score-t2_final_score)

        # Game Logistics
        pace = np.mean(game_rows.Pace.values)
        data.loc[row_index, 'Avg_Pace'] = pace
        avg_fg = np.mean(game_rows.EffFG.values)
        data.loc[row_index, 'Avg_EFG'] = avg_fg
        start_time = game_rows.Game_Time.values[0]
        data.loc[row_index, 'Start_Time'] = game_rows.Game_Time.values[0]
        data.loc[row_index, 'Total_Fouls'] = sum(game_rows.Fouls.values)

        # Team Winning %
        wins = game_rows.Wins_Entering_Gm.values
        losses = game_rows.Losses_Entering_Gm.values
        team1_total = wins[0] + losses[0]
        team2_total = wins[1] + losses[1]
        if team1_total == 0:
            team1_wp = 0.5
        else:
            team1_wp = wins[0]/team1_total
        if team2_total == 0:
            team2_wp = 0.5
        else:
            team2_wp = wins[1]/team2_total
        data.loc[row_index, 'Avg_Win%'] = np.mean([team1_wp, team2_wp])
        data.loc[row_index, 'Win%_Diff'] = abs(team1_wp-team2_wp)
        data.loc[row_index, 'First_Five_Games'] = team1_total <= 5

        # Number of Overtimes
        extra_minutes = game_rows.Team_Minutes.values[0] - 240
        Num_OT = round(extra_minutes/25)
        data.loc[row_index, 'Num_OT'] = Num_OT

        # Game Date
        game_date = row['Game_Date'].date()
        opening_day = [datetime.date(2016,10,25), datetime.date(2017,10,17)]
        if game_date in opening_day:
            data.loc[row_index, 'is_opening_day'] = True
        else:
            data.loc[row_index, 'is_opening_day'] = False

        # Allstar Data
        num_allstars = sum(player_rows.ASG_Team.values)
        allstar_rows = player_rows.loc[player_rows['ASG_Team'] == 1]
        num_active_allstars = sum(allstar_rows.Active_Status.values)
        data.loc[row_index, 'Num_Allstars'] = num_allstars
        data.loc[row_index, 'Active_Allstars'] = num_active_allstars

        # PER
        '''
        active_players = player_rows.loc[(player_rows['Active_Status'] == 1) & \
                (~player_rows['Minutes'].isnull) & (player_rows['Minutes'] != 0)]

        per = 0
        for player_index, player_row in active_players.iterrows():
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
        per_per = per/active_players.shape[0]
        data.loc[row_index, 'Total_PER'] = per
        data.loc[row_index, 'Avg_PER'] = per_per
        '''

    cols = data.columns.tolist()

    if option == 'train':
        data.to_csv('all_game_data.csv')
    else:
        data.to_csv('test_set_new.csv')

def main():
    update_data()

if __name__ == '__main__':
    main()
