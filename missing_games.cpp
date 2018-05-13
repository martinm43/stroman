 #include <string>
 #include <iostream>
 #include <stdio.h>
 #include <sqlite3.h>

 using namespace std;
 
 static int callback(void *NotUsed, int argc, char **argv, char **azColName){
   int i;
   for(i=0; i<argc; i++){
     printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
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
   string SQLStatement("SELECT * FROM POSTPHONED_GAMES_LOCAL"); 

   /* No longer necessary as we're using arguments in code
   if( argc!=3 ){
     fprintf(stderr, "Usage: %s DATABASE SQL-STATEMENT\n", argv[0]);
     return(1);
   }
   */

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







