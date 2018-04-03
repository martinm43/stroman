# coding: utf-8

"""
This file has been stripped to provide the solution to the Peewee operational error "too many SQL variables"
allowing for the insertion of a large number of dicts containing game data all at once.
Note that the "get max SQL variables" functionality appears to only work on certain platforms
"""

#Upsert the values, using the max number allowed by the system.
def big_inserter(db,SQLITE_MAX_VARIABLE_NUMBER,PeeweeClassObject,list_of_dicts):
  with db.atomic() as txn:
      size = (SQLITE_MAX_VARIABLE_NUMBER // len(list_of_dicts[0])) -1
      # remove one to avoid issue if peewee adds some variable
      for i in range(0, len(list_of_dicts), size):
          PeeweeClassObject.insert_many(list_of_dicts[i:i+size]).upsert().execute()
      return
        
