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
    string _team_name;
    string _mlbgames_name;
    string _abbreviation;
    string _division;
    string _league;

public:

    Team(int team_id, string team_name, string mlbgames_name, 
            string abbreviation, string division, string league):
        _team_id(team_id), _team_name(team_name), _mlbgames_name(mlbgames_name), 
            _abbreviation(abbreviation), _division(division), _league(league) {}

    int get_team_id() const {return _team_id;}
    string get_team_name() const {return _team_name;}
    string get_mlbgames_name() const {return _mlbgames_name;}
    string get_abbreviation() const {return _abbreviation;}
    string get_division() const {return _division;}
    string get_league() const {return _league;}

};

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    vector<Game> games;
    vector<Team> teams;

    //SQLite connection stuff
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

    while ((rc=sqlite3_step(stmt)) == SQLITE_ROW) {
        //Writing out the games to the screen (temporary for now, just for error checking)
        cout << "Away team id: " << sqlite3_column_int(stmt,1) << endl;
        cout << "Away team runs scored: " << sqlite3_column_int(stmt,2) << endl;
        cout << "Home team id: "<< sqlite3_column_int(stmt,3) << endl;
        cout << "Home team runs scored: " << sqlite3_column_int(stmt,4) << endl;

        //Store in our vector
        int away_team_id = sqlite3_column_int(stmt,1);
        int away_runs = sqlite3_column_int(stmt,2);
        int home_team_id = sqlite3_column_int(stmt,3);
        int home_runs = sqlite3_column_int(stmt,4);
        games.push_back(Game(away_team_id,away_runs,home_team_id,home_runs));
    }
    if (rc != SQLITE_DONE) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;   
    }
 
    /* 
    Statement number two, initializing the list of teams 
    */

    SQLStatement = "SELECT team_id, team_name, mlbgames_name, abbreviation, division, league from teams;";

    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    int nrows = 1;    

    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {


         cout << sqlite3_column_int(stmt,1)+1 << endl;
         cout << sqlite3_column_text(stmt,2) << endl;
         cout << sqlite3_column_text(stmt,3) << endl;
         cout << sqlite3_column_text(stmt,4) << endl;
         cout << sqlite3_column_text(stmt,5) << endl;
         cout << sqlite3_column_text(stmt,6) << endl;


        /* code that does not work, and associated runtime error.
        terminate called after throwing an instance of 'std::logic_error'
        what():  basic_string::_M_construct null not valid
        Aborted (core dumped)

        int team_id = sqlite3_column_int(stmt,1);
        string team_name = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,2)));
        string mlbgames_name = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,3)));
        string abbreviation = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,4)));
        string division = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,5)));
        string league = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,6)));
        teams.push_back(Team(team_id,team_name,mlbgames_name,abbreviation,division,league));
        */

    }

    if (rc != SQLITE_DONE) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;   
    }

    sqlite3_finalize(stmt);

return 0;
}
