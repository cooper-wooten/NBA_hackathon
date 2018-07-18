game.df = read.csv("game_data.csv")
player.df = read.csv("player_data.csv")
test = read.csv("new_test.csv")
train = read.csv("new_train.csv")
international = read.csv("International.csv")
twitter.df = read.csv("nba_twitter_account.csv")

# Make a new test data that contains country information

# countries = unique(train$Country)
# new_test = matrix(nrow = 0, ncol = length(colnames(train)[1:6]))
# colnames(new_test) = colnames(train)[1:6]
# 
# for(i in nrow(test)) {
#     season = test$Season[i]
#     game = test$Game_ID[i]
#     date = test$Game_Date[i]
#     away = test$Away_Team[i]
#     home = test$Home_Team[i]
#     for(country in countries) {
#         new_test = rbind(new_test, list(season = season, game = game, date = date, away = away, home = home, country = country))
#     }
# }

# Add whether that team won or lost in the game dataset
# teams = as.vector(unique(game$Team))
# for (row in game) {
#
# }

# countries = unique(train$Country)
# home_teams = unique(train$Home_Team)
# 
# home_data = matrix(nrow = 0, ncol = length(countries) + 1)
# colnames(home_data) = c("Country", as.character(countries))
# 
# for (team in home_teams)
# {
#   #team = home_teams[i]
#   this.list = c(team)
#   for (country in countries)
#   {
#     s = subset(train, train$Country == country & train$Home_Team == team)
#     total.viewers = sum(s$Rounded.Viewers)
# 
#     this.list = c(this.list, total.viewers)
#   }
#   home_data = rbind(home_data, this.list)
# }
# # home_data = as.character(home_teams)
# 
# country_dist = data.frame(home_data)

# Draw the distribution of countries factored on teams
# library(ggplot2)
# library(randomcoloR)
# 
# col.palette = distinctColorPalette(length(country_dist))
# 
# viewer.count = table(country_dist$CLE, country_dist$GSW)
# barplot(viewer.count, col=col.palette[1:2])
# 
# barplot(country_dist$LAC)
# lines(country_dist$CLE)
# for (i in 1:length(colnames(country_dist))) {
#     country = colnames(country_dist)[i]
# 
#     print(gg + geom_bar(aes(x = rownames(country_dist), y = country_dist[, country]), col=col.palette[i], stat="identity") +
#         labs(x = "Countries", y = country))
# }
# 
# ggplot(country_dist) +
#     geom_bar(aes(x = rownames(country_dist), y = country_dist[, "DAL"]), stat="identity")
# 
# 
# ggplot(country_dist) +
#     geom_bar(aes(x = rownames(country_dist), y = ATL), stat="identity")
# 
# 
# # Find the total number of fouls per each game
# game.ids = new.train$Game_ID
# find.fouls = function(player_df) {
#     fouls = c()
#     for (g.id in game.ids) {
#         subsetted = subset(player_df, Game_ID == g.id)
#         total.fouls = sum(subsetted$Personal_Fouls)
#         fouls = c(fouls, total.fouls)
#     }
#     return(fouls)
# }
# fouls = find.fouls(player)
# new.train$total_fouls = fouls
# new.train$away = levels(new.train$Away_Team)

# Function for finding distribution of viewerships from each country for each team
find.country.distribution = function(df, is.home) {
    countries = c(levels(unique(df$Country)))
    teams = ifelse(rep(is.home, length(unique(df$Home_Team))), c(levels(unique(df$Home_Team))), c(levels(unique(df$Away_Team))))
    # Matrix of distribution of viewers from each country, where first column is team
    dist.mat = matrix(nrow = 0, ncol = length(countries) + 1)
    colnames(dist.mat) = c("Team", countries)

    for (t in teams) {
        this.row = c(t)
        for (country in countries) {
            subsetted = subset(df, as.character(df$Country) == country & as.character(df$Home_Team) == t)
            total.viewers = sum(subsetted$Rounded.Viewers)

            this.row = c(this.row, total.viewers)
        }
        dist.mat = rbind(dist.mat, this.row)
    }
    rownames(dist.mat) = seq(1, nrow(dist.mat))

    return(data.frame(dist.mat, stringsAsFactors=F))
}

# Function to make a distributino of two teams
make.distribution.of.two = function(home, away, team) {
    subsetted.home = subset(home, home$Team == team)
    print(subsetted.home)
    subsetted.away = subset(away, away$Team == team)
    print(subsetted.away)

    ggplot() +
        geom_col(data=subsetted.home, aes(x = variable, y = value, fill=team), color="Blue", position="dodge") +
        geom_col(data=subsetted.away, aes(x = variable, y = value, fill=team), color="Red", position="dodge")
}

# Function to find the number of active all-star players for each game and each team
# df is either train or test data that we're interested in
update.allstars = function(df, player.df, game.df) {
    game.ids = unique(df$Game_ID)
    
    num.all.star = sapply(game.ids, function(id) {
        this.game = subset(player.df, Game_ID == id)
        return(sum(this.game$ASG_Team != "None"))
    })
    df$Num_Allstars = num.all.star
    
    active.all.star = sapply(game.ids, function(id) {
        this.game = subset(player.df, Game_ID == id)
        return(sum(this.game$ASG_Team != "None" & this.game$Active_Status == "Active"))
    })
    df$Active_Allstars = active.all.star
    
    return(df)
}

# Function to find the number of international players for each team
update.internationals = function(df, international, player.df) {
    num.internationals = c()
    num.active.internationals = c()
    for (i in 1:nrow(df)) {
        game.id = df$Game_ID[i]
        this.game = subset(player.df, Game_ID == game.id) 
        
        home.team = df$Home_Team[i]
        away.team = df$Away_Team[i]
        
        subsetted = subset(international, Team == home.team | Team == away.team)
        # Total number of internationals 
        num.internationals = c(num.internationals, nrow(subsetted))
        # Active number of internationals
        active.subsetted = subset(this.game, Name %in% subsetted$Name & Active_Status == "Active")
        num.active.internationals = c(num.active.internationals, nrow(active.subsetted))
    }
    df$Num_Internationals = num.internationals
    df$Active_Internationals = num.active.internationals
    return(df)
}

change.date.to.numeric = function(df) {
    new.date = paste(as.character(df$Game_Date), as.character(df$Start_Time), sep=" ")
    df$Game_Date = as.numeric(as.POSIXct(new.date))
    df$Start_Time = NULL
    return(df)
}

# Set up twitter oauth
library(twitteR)
consumer.key = "kGlFqeLPOaiTUtLJY3MehG7M6"
consumer.secret = "MKizE8NlxQ6ZOPHrsHkgjRo9SXSWnXX5KSudun9EogB5f3oMIp"
access.token = "946052093961539589-CW2EiM7s5koqcAnSw355kJns0uf1ah0"
access.secret = "fPxzv1fkYLSYcJWHMTqVHSkXFqEs1xRUyqUAbR1Viyyfs"
setup_twitter_oauth(consumer.key, consumer.secret, access.token, access.secret)

update.twitter.followers = function(df, twitter.df, player.df) {
    # Main loop to find active players for each game and find twitter followers 
    home.followers = c()
    away.followers = c()
    for (i in 1:nrow(df)) {
        game.id = df$Game_ID
        home.team = df$Home_Team
        away.team = df$Away_Team
        
        home.subsetted = subset(player.df, Game_ID == game.id & Active_Status == "Active" & Team == home.team)
        away.subsetted = subset(player.df, Game_ID == game.id & Active_Status == "Active" & Team == away.team)
        
        home.twit = subset(twitter.df, Player %in% home.subsetted$Name)$Twitter
        away.twit = subset(twitter.df, Player %in% away.subsetted$Name)$Twitter
        
        home.twit.obj = sapply(home.twit, getUser)
        away.twit.obj = sapply(home.twit, getUser)
        
        home.twit.followers = sum(sapply(home.twit.obj, followersCount))
        away.twit.followers = sum(sapply(away.twit.obj, followersCount))
    }
    df$Home_Twit_Followers = home.twit.followers
    df$Away_Twit_Followers = away.twit.followers
    
    return(df)
}

new.train = update.twitter.followers(train, twitter.df, player.df)

# gg = ggplot(alpha=0.5)
# colors = c("Red", "Blue", "Green", "Purple", "black", "Orange")
# t = teams[1]
# new.df1 = df %>% subset(Home_Team == t | Away_Team == t) %>% group_by(Country) %>% summarise(sum = sum(Rounded_Viewers))
# p1 = geom_col(aes(x = new.df1$Country, y = new.df1$sum), colour=colors[1], position="dodge")
# 
# t = teams[2]
# new.df2 = df %>% subset(Home_Team == t | Away_Team == t) %>% group_by(Country) %>% summarise(sum = sum(Rounded_Viewers))
# p2 = geom_col(aes(x = new.df2$Country, y = new.df2$sum), colours=colors[2], position="dodge")
# 
# t = teams[3]
# new.df3 = df %>% subset(Home_Team == t | Away_Team == t) %>% group_by(Country) %>% summarise(sum = sum(Rounded_Viewers))
# p3 = geom_col(aes(x = new.df3$Country, y = new.df3$sum), colour=colors[3], position="dodge")
# 
# t = teams[4]
# new.df4 = df %>% subset(Home_Team == t | Away_Team == t) %>% group_by(Country) %>% summarise(sum = sum(Rounded_Viewers))
# p4 = geom_col(aes(x = new.df4$Country, y = new.df4$sum), colour=colors[4], position="dodge")
# 
# t = teams[5]
# new.df5 = df %>% subset(Home_Team == t | Away_Team == t) %>% group_by(Country) %>% summarise(sum = sum(Rounded_Viewers))
# p5 = geom_col(aes(x = new.df5$Country, y = new.df5$sum), colour=colors[5], position="dodge")
# 
# t = teams[6]
# new.df6 = df %>% subset(Home_Team == t | Away_Team == t) %>% group_by(Country) %>% summarise(sum = sum(Rounded_Viewers))
# p6 = geom_col(aes(x = new.df6$Country, y = new.df6$sum), colour=colors[6], position="dodge")
# 
# gg + p1 + p2 + p2 + p3 + p4 + p5 + p6
# # gg + p1 + p2 + p3
# 
