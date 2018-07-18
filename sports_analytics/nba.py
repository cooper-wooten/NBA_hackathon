import pandas as pd
import nbastruct as nb
import collections

def initialize_players(lineup_df):
    '''
    First initialize players from game_df
    '''
    players = dict()

    for ind, row in lineup_df.iterrows():
        player_id = row['Person_id']
        team_id = row['Team_id']

        players[player_id] = nb.Player(player_id, team_id)

    return players

def initialize_teams(lineup_df):
    teams = dict()

    for ind, row in lineup_df.iterrows():
        team_id = row['Team_id']
        teams[team_id] = nb.Team(team_id)

    return teams

def initialize_games(lineup_df, teams):
    games = dict()
    players = dict()

    home_id = None
    away_id = None
    game_set = False
    for ind, row in lineup_df.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        player_id = row['Person_id']

        # Firstly initialize games
        if game_id not in games.keys():
            # subset of the lineup_df where gameID matches
            games[game_id] = nb.Game(game_id)
            home_id = team_id
            away_id = None
            game_set = False
        elif team_id != home_id and game_set == False:
            away_id = team_id
            games[game_id].set_teams(teams[home_id], teams[away_id])
            # Rest parameters
            home_id = None
            away_id = None
            game_set = True

    return games

def play(lineup_df, game_df, games):
    for game_id, this_game in games.items():
        subset_df = game_df.loc[game_df['Game_id'] == game_id,]

        for ind, row in subset_df.iterrows():
            event_type = row['Event_Msg_Type']
            team_id = row['Team_id']
            period = row['Period']
            player1_id = row['Person1']
            player2_id = row['Person2']
            time = row['PC_Time']
            option1 = row['Option1'] # Points scored when shot made

            # Foul/Substituion/Free Throw done
            if this_game.fouled and this_game.foul_time != time:

                for (leaving, entering) in this_game.sub_todo:
                    this_game.substitute(leaving, entering)
                this_game.reset_foul()

            if event_type == 12: # start period
                this_game.update_lineup(lineup_df, period)

            elif event_type == 13: # End period
                this_game.end_period()

            elif event_type == 1: # made shot
                point = option1 if str(this_game.home) == team_id else -option1
                this_game.update_score(point)

            elif event_type == 6: # foul
                this_game.foul(time)

            elif event_type == 8: # substitution
                # Ehck if this player was ever in the game
                this_game.check_players(player1_id, player2_id, team_id)

                if not this_game.fouled:
                    this_game.substitute(this_game.players[player1_id],
                                         this_game.players[player2_id])
                else:
                    this_game.append_sub(this_game.players[player1_id],
                                         this_game.players[player2_id])

            elif event_type == 3: # free throw
                point = option1 if str(this_game.home) == team_id else -option1
                this_game.update_score(point)

    return games

def update_players_record(games):
    result = collections.OrderedDict()
    result['Game_id'] = list()
    result['Player_id'] = list()
    result['score'] = list()

    for game_id, this_game in games.items():
        # Scores that each player made from this game
        scores = {p_id:p.score for p_id, p in this_game.players.items()}

        for p_id, score in scores.items():
            result['Game_id'].append(str(this_game))
            result['Player_id'].append(p_id)
            result['score'].append(score)

    return result

def save_to_csv(result, filepath):
    print("Result saving to .csv at {}".format(filepath))
    df = pd.DataFrame(data = result)
    df.to_csv(filepath, index = False)

def parse(lineup_df_filepath, game_df_filepath, csv_filepath, save):
    lineup_df = pd.read_table(lineup_df_filepath, header = 0, sep = '\s+')
    game_df = pd.read_table(game_df_filepath, header = 0, sep = '\s+')

    teams = initialize_teams(lineup_df)
    games = initialize_games(lineup_df, teams)

    games_played = play(lineup_df, game_df, games)
    result = update_players_record(games)

    if save:
        save_to_csv(result, csv_filepath)

