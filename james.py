"""
Regression functions for calculating
binomial win percentages

Named after the pioneer Bill James.

"""

#Selection of mathematical models for MLB win predictions

def runs_regress(dpts):
  import math
  return 1/(1+math.exp(-1*(0.15+dpts*0.2)))

def SRS_regress(dSRS):
  import math
  return 1/(1+math.exp(-1*(0.15+dSRS*0.85)))

if __name__=='__main__':
  print(SRS_regress(2))
