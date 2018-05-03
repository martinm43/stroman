# coding: utf-8
import xlsxwriter
from datetime import datetime
from mlb_data_models import database
#database.execute_sql('select scheduled_date, home_team, away_team from'+\
#4                      'postphoned_games_local;')
result=database.execute_sql('select * from postphoned_games_local;')
x=[[i[9],i[1],i[2]] for i in result] #has to be crossreferenced with the view in sqlite3
x.sort(key=lambda i:i[0]) #sort by date

#datestring.
now=datetime.now()
now_str=now.strftime('%Y-%m-%d')

#Output a formatted file that you can show and view easily - Write an xlsx
workbook=xlsxwriter.Workbook('Missed_Games_Worksheet.xlsx')
worksheet=workbook.add_worksheet()

#bold format for headers and appropriate widths
bold14=workbook.add_format({'bold':True,'font_size':14})
bold14.set_align('center')
bold14.set_align('vcenter')
bold14.set_text_wrap()

#Set lengths
worksheet.set_column('A:A',22)
worksheet.set_column('B:B',15)
worksheet.set_column('C:C',15)
worksheet.set_column('D:D',15)
worksheet.set_column('E:E',15)

#Centering
centformat=workbook.add_format()
centformat.set_align('center')

#Number formats
diffformat=workbook.add_format()
pctformat=workbook.add_format()

diffformat.set_num_format('0.00')
pctformat.set_num_format('0.00%')

diffformat.set_align('center')
pctformat.set_align('center')

#Add headers to the xlsx.
worksheet.write('A1','Date',bold14)
worksheet.write('B1','Home Team',bold14)
worksheet.write('C1','Away Team',bold14)
worksheet.write('D1','Away Team Runs',bold14)
worksheet.write('E1','Home Team Runs',bold14)

row=1
col=0

#Write the data
for date,ht,at in (x):
  col=0
  worksheet.write(row,col,date)
  worksheet.write(row,col+1,ht,centformat)
  worksheet.write(row,col+2,at,centformat)
  row += 1

workbook.close()