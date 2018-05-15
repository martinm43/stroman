#include <cstdlib>
#include <cmath>
#include <ctime>
#include <iostream>

#define ITER 10000

using namespace std;

double uniformRandom()
{
  return ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
}

int main()
{
  srand(time(NULL));

  int wins[3] = {0,0,0}; //test array for storing wins

  double gameslist[5][3] = { //home team win odds, home team, away team
    {0.4,1,2},
    {0.6,3,2},
    {0.7,3,1},
    {0.3,2,1},
    {0.6,2,3},
  };

  for(int i_iter=0;i_iter<ITER;i_iter++){
    for(int i=0;i<5;i++){
        if (gameslist[i][0] > uniformRandom()){
            wins[(int) gameslist[i][1] - 1]+=1;  
        }
        else {
            wins[(int) gameslist[i][2] - 1]+=1;  
        }
    }
  }

  for(int i=0;i<3;i++){
     cout << "Team " << i+1 << "has an average winning percentage of " << 
            (double) wins[i]/(ITER*3) << endl;
  }

  cout << i_iter << " iterations were completed!" << endl;
  return 0;
}
