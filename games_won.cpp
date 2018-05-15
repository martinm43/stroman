#include <iostream>
#include <armadillo>
#include <string>
#include <stdio.h>
#include <sqlite3.h>

using namespace std;

static int callback(void *NotUsed, int argc, char **argv, char **azColName){
   int i;
   for(i=0; i<argc; i++){
     printf("%s = %s \n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   printf("\n");
   return 0;
}


int main(int argc, char **argv){
   sqlite3 *db;
   char *zErrMsg = 0;
   int rc;

   //replacing argv[1]
   string DatabaseName("mlb_data.sqlite");
   //replacing argv[2]
   string SQLStatement("SELECT away_team, away_runs, home_team, home_runs "
                       "FROM games WHERE (scheduled_date < datetime('now')) "
                       "AND NOT (away_runs=0 and home_runs=0);");

   rc = sqlite3_open(DatabaseName.c_str(), &db);
   if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return(1);
   }
   rc = sqlite3_exec(db, SQLStatement.c_str(), callback, 0, &zErrMsg);
   if( rc!=SQLITE_OK ){
     fprintf(stderr, "SQL error: %s\n", zErrMsg);
     sqlite3_free(zErrMsg);
   }
   sqlite3_close(db);


   return 0;
 }







