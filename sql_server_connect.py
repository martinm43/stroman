#Updating the SQL Server, using upsert functionality taken from:
#https://stackoverflow.com/questions/43899189/access-database-upsert-with-pyodbc

from apitool.lcbo_list_updater import lcbo_list_updater
import pyodbc 

#Obtain the data required.
productslist = lcbo_list_updater('products',1,1)
all_fields = productslist[0].keys()
all_fields.remove('id')
data_fields=all_fields
key_fields = ['id']

#Update type statements.
update_set = ','.join(['[' + x + ']=?' for x in data_fields])
update_where = ' AND '.join(['[' + x + ']=?' for x in key_fields])
sql_update = "UPDATE [products] SET " + update_set + " WHERE " + update_where

#print(sql_update)

#Insert type statements.
insert_fields = ','.join(['[' + x + ']' for x in (data_fields + key_fields)])
insert_placeholders = ','.join(['?' for x in (data_fields + key_fields)])
sql_insert = "INSERT INTO [products] (" + insert_fields + ") VALUES (" + insert_placeholders + ")"
#print(sql_insert)

#Connect to the server.
cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                      "Server=Owner-PC;"
                      "Database=MS_lcbo_db;"
                      "Trusted_Connection=yes;")

crsr = cnxn.cursor()

#Begin UPDATE OR INSERT process with the data obtained.
productslist = [productslist[0]]
for p in productslist:
    for k, v in p.iteritems():
        if v == None:
            print k, v

for p in productslist:
    p_id = p['id'] #get id
    p.pop('id') #remove id
    print p.keys()
    params = p.values()
    params.append(p_id)
    params = ["" if x == None else x for x in params]
    print params
    
    print sql_update.format(params)
    crsr.execute(sql_update, params)
    if crsr.rowcount > 0:
        print('Existing row updated.')
    else:
        crsr.execute(sql_insert, params)
        print('New row inserted.')
    crsr.commit() 