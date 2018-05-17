/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <stdio.h>
#include <iostream>
#include <vector>
#include <sqlite3.h>
#include <string>

using namespace std;

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

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    //Two vectors for holding key information to be used later
    vector<Game> games;
    vector<Team> teams;

    //Name of the database
    string DatabaseName("mlb_data.sqlite");

    string SQLStatement("SELECT away_team, away_runs, home_team, home_runs "
                       "FROM games WHERE (scheduled_date < datetime('now')) "
                       "AND NOT (away_runs=0 and home_runs=0);");

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
        cout << "Away team id: " << sqlite3_column_int(stmt,0) << endl;
        cout << "Away team runs scored: " << sqlite3_column_int(stmt,1) << endl;
        cout << "Home team id: "<< sqlite3_column_int(stmt,2) << endl;
        cout << "Home team runs scored: " << sqlite3_column_int(stmt,3) << endl;

        //Store in our vector
        int away_team_id = sqlite3_column_int(stmt,0);
        int away_runs = sqlite3_column_int(stmt,1);
        int home_team_id = sqlite3_column_int(stmt,2);
        int home_runs = sqlite3_column_int(stmt,3);
        games.push_back(Game(away_team_id,away_runs,home_team_id,home_runs));
    }

    cout << "Games successfully entered" << endl;

    /* - Not sure why this is not usable here.
    if (rc != SQLITE_DONE) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;   
    }

    sqlite3_finalize(stmt);
 
    /* 
    Statement number two, initializing the list of teams 
    */

    //SQLStatement = "SELECT team_id, team_name, mlbgames_name, abbreviation, division, league from teams;";

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

    int nrows = 1;    

    while (sqlite3_step(stmt) == SQLITE_ROW) {


         cout << sqlite3_column_int(stmt,0)+1 << endl;
         cout << sqlite3_column_text(stmt,1) << endl;
         cout << sqlite3_column_text(stmt,2) << endl;
         cout << sqlite3_column_text(stmt,3) << endl;
         cout << sqlite3_column_text(stmt,4) << endl;
         cout << sqlite3_column_double(stmt,5) << endl;

        /* code that does not work, and associated runtime error.
        terminate called after throwing an instance of 'std::logic_error'
        what():  basic_string::_M_construct null not valid
        Aborted (core dumped)

        Trying this using, uh, the fact that C arrays start at 0.

        */

        int team_id = sqlite3_column_int(stmt,0);
        string mlbgames_name = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,1)));
        string abbreviation = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,2)));
        string league = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,3)));
        string division = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,4)));
        float rating = sqlite3_column_double(stmt,6);
        teams.push_back(Team(team_id,mlbgames_name,abbreviation,league,division,rating));
    }


    sqlite3_finalize(stmt);

    if (rc == SQLITE_OK) {
        cerr << "Selections are complete." << endl;
    }

    cout << teams[2].get_mlbgames_name() << endl;

return 0;
}
