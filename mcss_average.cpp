
/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <iomanip>
#include <stdio.h>
#include <iostream>
#include <vector>
#include <sqlite3.h>
#include <string>
#include <math.h>
#include <armadillo>

#define MAX_ITER 100000

using namespace std;
using namespace arma;

double uniformRandom() {
  return ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
}

class Game{
private:

   int _away_team_id;
   int _away_runs;
   int _home_team_id;
   int _home_runs;

public:
   Game(int away_team_id, int away_runs, int home_team_id, int home_runs): 
     _away_team_id(away_team_id), _away_runs(away_runs), _home_team_id(home_team_id), _home_runs(home_runs) {}

   int get_away_team_id() const {return _away_team_id;}
   int get_away_runs() const {return _away_runs;}
   int get_home_team_id() const {return _home_team_id;}
   int get_home_runs() const {return _home_runs;}

};

class Team{
private:

    int _team_id;
    string _mlbgames_name;
    string _abbreviation;
    string _division;
    string _league;
    float _rating;

public:

    Team(int team_id, string mlbgames_name, 
            string abbreviation, string division, string league, 
            float rating):
        _team_id(team_id), _mlbgames_name(mlbgames_name), 
            _abbreviation(abbreviation), _division(division), 
            _league(league), _rating(rating) {}

    int get_team_id() const {return _team_id;}
    string get_mlbgames_name() const {return _mlbgames_name;}
    string get_abbreviation() const {return _abbreviation;}
    string get_division() const {return _division;}
    string get_league() const {return _league;}
    float get_rating() const {return _rating;}
};

double SRS_regress(double rating_away, double rating_home)
{
    float m=0.35;
    float b=-0.2; 
    return (double) 1.0/(1.0 + exp(-1*(m*(rating_home-rating_away)+b)));
}


int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    //Random info
    srand(time(NULL));

    //Two vectors for holding key information to be used later
    vector<Game> games;
    vector<Team> teams;

    // Matrix examples.
    mat Head_To_Head = zeros<mat>(30,30);
    mat MCSS_Head_To_Head = zeros<mat>(30,30);
    mat Sim_Total = zeros<mat>(30,30);
    mat debug_total = zeros<mat>(30,30);

    //Name of the database
    string DatabaseName("mlb_data.sqlite");

    /* S1 - GETTING LIST OF KNOWN WINS */
    string SQLStatement("SELECT away_team, away_runs, home_team, home_runs "
                       "FROM games WHERE scheduled_date <= datetime('now','-1 day');");

    sqlite3_stmt *stmt;

    rc = sqlite3_open(DatabaseName.c_str(), &db);
    if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return(1);
    }
    
    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        //Writing out the games to the screen (temporary for now, just for error checking)
        //cout << "Away team id: " << sqlite3_column_int(stmt,0) << endl;
        //cout << "Away team runs scored: " << sqlite3_column_int(stmt,1) << endl;

        //Store in our vector
        int away_team_id = sqlite3_column_int(stmt,0);
        int away_runs = sqlite3_column_int(stmt,1);
        int home_team_id = sqlite3_column_int(stmt,2);
        int home_runs = sqlite3_column_int(stmt,3);
        games.push_back(Game(away_team_id,away_runs,home_team_id,home_runs));

        if (home_runs > away_runs)
            Head_To_Head.row(home_team_id-1)[away_team_id-1]++;
        else
            Head_To_Head.row(away_team_id-1)[home_team_id-1]++;
    }

    cout << "Games successfully entered" << endl;
    //cout << "Head to Head Matrix:" << endl;
    //cout << Head_To_Head << endl;

    /* S2 - GETTING THE TEAMS AND THEIR MOST RECENT RATINGS */

    SQLStatement =  "select t.id,t.mlbgames_name,t.abbreviation,t.league,t.division,s.rating "
                    "from teams as t "
                    "inner join SRS_Ratings as s "
                    "on s.team_id=t.id "
                    "where s.rating <> 0 "
                    "and s.rating_date = (select rating_date from SRS_ratings "
                    "order by rating_date desc limit 1)";


    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);

    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {

         //Debug print to screen - example
         //cout << sqlite3_column_int(stmt,0)+1 << endl;
         //cout << sqlite3_column_text(stmt,1) << endl;

        //Write information into the vectors.
        int team_id = sqlite3_column_int(stmt,0);
        string mlbgames_name = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,1)));
        string abbreviation = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,2)));
        string league = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,3)));
        string division = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,4)));
        float rating = sqlite3_column_double(stmt,6);
        teams.push_back(Team(team_id,mlbgames_name,abbreviation,league,division,rating));
    }

    /* S3 - GETTING THE NUMBER OF FUTURE GAMES FOR S4 */

    SQLStatement =  "select count(*) from "
                    "games as g inner join srs_ratings as ra on "
                    "ra.team_id=g.away_team inner join srs_ratings as rh on "
                    "rh.team_id=g.home_team where g.scheduled_date >= datetime('now') "
                    "and ra.rating_date = (select max(rating_date) from srs_ratings) "
                    "and rh.rating_date = (select max(rating_date) from srs_ratings);";

    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);

    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    int num_future_games;

    while (sqlite3_step(stmt) == SQLITE_ROW) {

        num_future_games = sqlite3_column_int(stmt,0);
    }

    cout << "Number of games to predict: " << num_future_games << endl;

    mat future_games = zeros<mat>(num_future_games,4);

    sqlite3_finalize(stmt);

    if (rc == SQLITE_OK) {
        cerr << "Game processing is complete." << endl;
    }
    /* S3 - GETTING FUTURE GAMES AND THEIR ASSOCIATED RATINGS */

    SQLStatement =  "select g.away_team, ra.rating, g.home_team, rh.rating from "
                    "games as g inner join srs_ratings as ra on "
                    "ra.team_id=g.away_team inner join srs_ratings as rh on "
                    "rh.team_id=g.home_team where g.scheduled_date >= datetime('now') "
                    "and ra.rating_date = (select max(rating_date) from srs_ratings) "
                    "and rh.rating_date = (select max(rating_date) from srs_ratings) "
                    "order by g.id asc";

    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);

    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    int future_games_row = 0;

    while (sqlite3_step(stmt) == SQLITE_ROW) {

         //Debug print to screen - example (away team, away rtg, home team, home rtg)
         future_games.row(future_games_row)[0] = sqlite3_column_int(stmt,0);
         future_games.row(future_games_row)[1] = sqlite3_column_double(stmt,1);
         future_games.row(future_games_row)[2] = sqlite3_column_int(stmt,2);
         future_games.row(future_games_row)[3] = sqlite3_column_double(stmt,3);
         future_games_row++;
         //cout << future_games_row << endl;
    }

    sqlite3_finalize(stmt);

    if (rc == SQLITE_OK) {
        cerr << "Processing of future games' binomial win probabilities is complete." << endl;
    }
    

    for(int x_iter=0;x_iter<MAX_ITER;x_iter++){
    /* S5 - Monte Carlo Simulation */
        //set mcss head to head matrix to zero
        MCSS_Head_To_Head.zeros();
        for(int i=0;i<num_future_games;i++)
        {
            int away_team_id = future_games.row(i)[0]-1;
            float away_team_rtg = future_games.row(i)[1];
            int home_team_id = future_games.row(i)[2]-1;
            float home_team_rtg = future_games.row(i)[3];

            //cout << away_team_id << endl;
            //cout << away_team_rtg << endl;
            //cout << home_team_id << endl;
            //cout << home_team_rtg << endl;

            if (uniformRandom()<SRS_regress(away_team_rtg,home_team_rtg))
                MCSS_Head_To_Head.row(home_team_id)[away_team_id]++;
            else
                MCSS_Head_To_Head.row(away_team_id)[home_team_id]++;
        }

        debug_total.zeros();
        debug_total = MCSS_Head_To_Head+Head_To_Head;
        Sim_Total += debug_total;
    }
        cout << sum(Sim_Total.t()/MAX_ITER) << endl;

return 0;
}