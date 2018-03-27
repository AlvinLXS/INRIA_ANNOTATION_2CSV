#coding：utf-8
#使用r前缀，不考虑转义问题

import os
import re
import numpy as np

def iterbrowse(path):
    for home, dirs, files in os.walk(path):
        for filename in files:
            yield os.path.join(home, filename)


testcount=1
outpath='I:/test/ANA/'
for fullname in iterbrowse("I:/INRIADATA/INRIADATA/original_images/test/annotations"):
    f = open(fullname)
    c = f.read()

    t = re.search(r'Objects with ground truth : (\d)', c)
    count = int(t.group(1))
    m = re.findall(r'(\(Xmax,\sYmax\))\s:\s\(([^\)]+)\)\s-\s\(([^\)]+)\)', c)
    bbs = []
    for i in range(count):
        min = list(map(int, m[i][1].split(',')))
        xmin = min[0]
        ymin = min[1]
        max = list(map(int, m[i][2].split(',')))
        xmax = max[0]
        ymax = max[1]
        height = xmax - xmin
        width = ymax - ymin
        bbs.append([xmin, ymin, width, height, 1])

    name1 = re.search(r'crop_\d{6}', fullname)
    name2 = re.search(r'crop\d{6}', fullname)
    name3 = re.search(r'person_\d{3}', fullname)
    name4 = re.search(r'person_and_bike_\d{3}', fullname)
    if(name1!=None):
        name = outpath + name1.group()+'.csv'
    elif(name2!=None):
        name = outpath + name2.group() + '.csv'
    elif(name3!=None):
        name = outpath + name3.group() + '.csv'
    elif(name4!=None):
        name = outpath + name4.group() + '.csv'


    bbs=np.array(bbs)

    np.savetxt(name,bbs,fmt='%d',delimiter = ',')








