#include <iostream>
#include <armadillo>

using namespace std;
using namespace arma;

int main()
  {
  mat A = randu<mat>(4,5);
  mat B = randu<mat>(4,5);
  
  //cout << A*B.t() << endl;


  A.row(0)[0] = 420.00;
  cout << A.row(0)[0] << endl;
  
  return 0;
  }
