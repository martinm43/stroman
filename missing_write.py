# coding: utf-8
from mlb_data_models import database
database.execute_sql('select * from postphoned_games_local;')
result=database.execute_sql('select * from postphoned_games_local;')
x=[i for i in result]
x
import xlsxwriter
