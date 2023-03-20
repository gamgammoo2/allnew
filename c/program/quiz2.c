#include <stdio.h>
#include "libcheckprime.h"

void main() {
  while(1) {
    int n;
    printf("Input Number : ");
    scanf("%d", &n);
    if (n==0)
      break;
    if(checkprime(n)==n)
      printf("%d is prime \n", n);
    else
      printf("%d is not prime \n", n);
  }
}
