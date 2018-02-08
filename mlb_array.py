# coding: utf-8
get_ipython().magic(u'load mlb_array.py')
# %load mlb_array.py
# %load mlb_array.py
import pandas as pd
mlb_schedule_2018=pd.read_excel('MLB_schedule_2018_1_.xls')
mlb_array=mlb_schedule_2018.as_matrix()
mlb_games_list=mlb_array[:,4].tolist()
mlb_games_list_bos=[x for x in mlb_games_list if str(x) != 'nan']
[x.replace('@','') for x in mlb_games_list_bos]
clean_bos_list=[x.replace('@','') for x in mlb_games_list_bos]
len(clean_bos_list)
list(set(clean_bos_list))
list(set(clean_bos_list))
mlb_games_list=mlb_array[:,17].tolist()
mlb_games_list_ari=[x for x in mlb_games_list if str(x) != 'nan']
clean_ari_list=[x.replace('@','') for x in mlb_games_list_ari]
list(set(clean_ari_list))
clean_bos_list+clean_ari_list
nl_al_teams=list(set((clean_bos_list+clean_ari_list)))
nl_al_teams
len(nl_al_teams)
nl_al_teams.sort()
nl_al_teams
nl_al_teams.add('Bos')
nl_al_teams.append('Bos')
nl_al_teams
nl_al_teams.pop('Bos')
nl_al_teams.remove('Bos')
nl_al_teams
nl_al_teams.append(u'Bos')
nl_al_teams
nl_al_teams.append(u'Ari')
nl_al_teams
nl_al_teams.sort()
