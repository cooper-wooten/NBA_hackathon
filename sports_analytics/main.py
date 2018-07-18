import optparse
import nba


def main():
    # Add CLI options

    parser = optparse.OptionParser()
    # Lineup data filepath
    parser.add_option('-l',
        action="store", dest="lineup_filepath",
        help="query string", default="nba_lineup.txt")
    # playbyplay data filepath
    parser.add_option('-q',
        action="store", dest="playbyplay_filepath",
        help="query string", default="nba_playbyplay.txt")
    # output filepath
    parser.add_option('-o',
        action="store", dest="result_filepath",
        help="query string", default="nba_result.csv")
    # Save or not
    parser.add_option('-s',
        action="store", dest="save",
        help="query string", default="True")

    options, args = parser.parse_args()
    # Run the main program
    nba.parse(options.lineup_filepath,
              options.playbyplay_filepath,
              options.result_filepath,
              bool(options.save))

if __name__=='__main__':
    main()
