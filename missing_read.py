#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:16:00 2018

@author: martin
"""

from __future__ import print_function
import os
import xlrd

fname = os.path.dirname(os.path.realpath(__file__)) + \
    '/' + 'Missed_Games_Worksheet.xlsx'

# Open the workbook
xl_workbook = xlrd.open_workbook(fname)

data_rows = []
row_number = 1
xl_sheet = xl_workbook.sheet_by_index(0)

for i in range(1, xl_sheet.nrows):
    row = xl_sheet.row(i)
    row_dict = {'scheduled_date': row[0].value, 'away_team': row[1].value,
                'home_team': row[2].value, 'away_runs': row[3].value,
                'home_runs': row[4].value}
    data_rows.append(row_dict)
