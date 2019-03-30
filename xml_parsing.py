import os
import xml.etree.cElementTree as ET
import xml.dom.minidom
import numpy as np

filename = "data/en/truth-train.txt"


table = np.genfromtxt(filename, delimiter = ':::', dtype = 'U20')
print(table)

def readData()
    filepath = "data/en/"
    for id in table[:,0]:
    f = filepath + id
    read 
