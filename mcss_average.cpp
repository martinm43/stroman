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
   Game(int away_team_id, int away_runs, int home_team_id, int home_runs): _away_team_id(away_team_id), _away_runs(away_runs), _home_team_id(home_team_id), _home_runs(home_runs) {}
};

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    vector<Game> games;

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

    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
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
        // if you return/throw here, don't forget the finalize
        sqlite3_finalize(stmt);
        return 1;   
    }
    sqlite3_finalize(stmt);
 
    cout<<games[0]<<endl;

return 0;
}
