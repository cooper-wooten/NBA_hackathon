class Team():
    # players on the court
    def __init__(self, team_id):
        self.team_id = team_id
        self.players = dict()

    def __str__(self):
        return self.team_id

    def add_player(self, player):
        self.players[str(player)] = player

    def remove_player(self, player):
        self.lineup.remove(player)

    def print_players(self):
        for k,v in self.players:
            print("player: " + k + "score" + v)

class Player():
    def __init__(self, player_id, team_id):
        self.player_id = player_id
        self.team_id = team_id
        # self.onCourt = False
        self.score = 0

        self.attended_games = dict()

    def __str__(self):
        return self.player_id

    def update_score(self, point):
        self.score += point

    def update_game(self, game):
        self.attended_games[str(game)] = game

class Game():
    def __init__(self, game_id):
        self.game_id = game_id

        self.home_oncourt = list()
        self.away_oncourt = list()

        self.players = dict()
        self.sub_todo = list() # In case of free throws

        self.fouled = False
        self.foul_time = 0

    def __str__(self):
        return self.game_id

    def set_teams(self, home, away):
        self.home = home
        self.away = away

    # Check if given players are already contained in self.players
    def check_players(self, player1_id, player2_id, team_id):
        for p_id in [player1_id, player2_id]:
            if p_id not in self.players.keys():
                self.players[p_id] = Player(p_id, team_id)

    def append_sub(self, leaving, entering):
        self.sub_todo.append((leaving, entering))

    def add_player(self, player):
        self.players[str(player)] = player

    def update_lineup(self, lineup_df, period):
        # Updates starting lineups for the beginning of each period
        starting_lineup = lineup_df.loc[(lineup_df['Period'] == period) &\
                                        (lineup_df['Game_id'] == self.game_id),]

        for ind, row in starting_lineup.iterrows(): # Has to be 10
            player_id = row['Person_id']
            team_id = row['Team_id']

            if team_id == str(self.home): # home player
                self.home_oncourt.append(player_id)
            else: # away player
                self.away_oncourt.append(player_id)

            this_player = Player(player_id, team_id)
            self.add_player(this_player)

    def update_score(self, point):
        # Update players dict instead of oncourt dict
        [self.players[p_id].update_score(point) for p_id in self.home_oncourt]
        [self.players[p_id].update_score(-point) for p_id in self.away_oncourt]

    def end_period(self):
        self.home_oncourt = list()
        self.away_oncourt = list()

    def substitute(self, leaving, entering):
        if str(leaving) in self.home_oncourt:
            self.home_oncourt.remove(str(leaving))
            self.home_oncourt.append(str(entering))
        else:
            self.away_oncourt.remove(str(leaving))
            self.away_oncourt.append(str(entering))

        self.add_player(entering)

    def foul(self, time):
        self.fouled = True
        self.foul_time = time

    def reset_foul(self):
        self.fouled = False
        self.foul_time = 0
        self.sub_todo = list()


