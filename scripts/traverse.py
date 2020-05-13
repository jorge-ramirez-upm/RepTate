import os
import py_compile
import shutil

# Set the directory you want to start from
rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
    #print('Found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith('.py'):
            if dirName=='.':
                print('%s' % fname)
            else:
                print('%s' % (dirName+os.sep+fname))
            a = py_compile.compile(dirName+os.sep+fname,cfile=dirName+os.sep+fname+'c')
            os.remove(dirName+os.sep+fname)
        
for dirName, subdirList, fileList in os.walk(rootDir):
    for dname in subdirList:
        if dname=='__pycache__':
            print(dirName+os.sep+dname)
            shutil.rmtree(dirName+os.sep+dname)
