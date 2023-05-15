import numpy as np

a = np.array([-1,3,2,-6])
b=np.array([3,6,1,2])
print('a= ',a)
print('b=',b)

A=np.reshape(a,[2,2])
B=np.reshape(b,[2,2])
print('A=',A)
print('B=', B)

A1=np.matmul(A,B)
B1=np.matmul(B,A)
print('A1=',A1)
print('B1=',B1)

a=np.reshape(a,[1,4])
b=np.reshape(b,[1,4]) #행렬에 차원을 부가함.
b2=np.transpose(b)
print('b2= ',b2)

R=np.matmul(a,b2)
print('R=',R)