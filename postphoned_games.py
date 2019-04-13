"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django
"""



from mlb_data_models import Team, database

# get the team rating data
query = database.execute_sql("select count(*) from postphoned_games_local")

postphoned_games = [i for i in query]

print("Number of postphoned games: "+str(i[0]))
