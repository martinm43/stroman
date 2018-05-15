/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <stdio.h>
#include <iostream>
#include <vector>
#include <sqlite3.h>
#include <string>

using namespace std;

//class Game(int away_team, int away_runs, int home_team, int home_runs)

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    //For what we choose to store the values in.
    //vector<Address> games;
    

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
        return 1;
    }
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        //int id = sqlite3_column_int(stmt, 0);
        //const char* name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        //const char* number = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        // let's assume number can be NULL:
        //addresses.push_back(Address(id, name, number ? number : ""));
        cout << "Away team id: " << sqlite3_column_int(stmt,1) << endl;
        cout << "Away team runs scored: " << sqlite3_column_int(stmt,2) << endl;
        cout << "Home team id: "<< sqlite3_column_int(stmt,3) << endl;
        cout << "Home team runs scored: " << sqlite3_column_int(stmt,4) << endl;
    }
    if (rc != SQLITE_DONE) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        // if you return/throw here, don't forget the finalize
    }
    sqlite3_finalize(stmt);

return 0;
}
