import numpy as np
f=np.load("linlin.npz")
Z=f['Z']
cnu=f['cnu']
data=f['data']

Z0=100
cnu0=1.0
indZ = (np.where(Z==Z0))[0][0]
indcnu = (np.where(cnu==cnu0))[0][0]

table=data[indZ]
ind1=1+indcnu*2
ind2=ind1+1
for i in range(len(table)):
    print(table[i][0], table[i][ind1], table[i][ind2])
