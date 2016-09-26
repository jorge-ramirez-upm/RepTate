import numpy as np
import glob

# Reads all the files of the precalculated linlin theory and saves them 
# in a more compact *.npz format

files=glob.glob("g*.dat")
flist={}
for file in glob.glob("g*.dat"):
    n = file.split('.')
    m = int(n[0][1:])
    flist[m]=file

Z=np.asarray(list(flist.keys()))
cnu=np.asarray([0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10])

data=[]    
for k in flist.keys():
    data.append(np.loadtxt(flist[k]))

np.savez_compressed("linlin.npz",Z=Z, cnu=cnu, data=data)
