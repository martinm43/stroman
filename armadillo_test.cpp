#include <iostream>
#include <armadillo>

using namespace std;
using namespace arma;

int main()
  {
  mat A = randu<mat>(4,5);
  mat B = randu<mat>(4,5);
  
  cout << A*B.t() << endl;

  A[1][3]=0;

  cout << A << endl;
  
  return 0;
  }
