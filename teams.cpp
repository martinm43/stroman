/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <stdio.h>
#include <iostream>
#include <vector>
#include <sqlite3.h>
#include <string>

using namespace std;

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    //SQLite connection stuff
    string DatabaseName("mlb_data.sqlite");

    string SQLStatement = "SELECT team_name from teams;";
    //string SQLStatement("SELECT away_runs FROM games WHERE NOT (away_runs=0 AND home_runs=0);");

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

    int nrows = 1;    

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        cout << sqlite3_column_text(stmt,0) << endl;
        nrows++;
    }

    cout << nrows << endl;
    sqlite3_finalize(stmt);

return 0;
}
