<<<<<<< HEAD
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
=======
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
>>>>>>> 0fef93778346d0b9215a4b64a4fae7c03faa1db9
