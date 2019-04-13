import pyodbc

cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                      "Server=Owner-PC;"
                      "Database=MS_mlb_data;"
                      "Trusted_Connection=yes;")

querystring = "select count(*) from postphoned_games_local"

crsr = cnxn.cursor()
crsr.execute(querystring)
for row in crsr:
    print(('Number of games missing from MSSQL Database: '+str(row[0])))
crsr.commit()
