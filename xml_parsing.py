import os
import xml.etree.cElementTree as ET
import xml.dom.minidom
import numpy as np

def readData(id_list):
    filepath = "data/en/"
    #data in the form {'id': 'tweet body'}
    data_train = {}
    for id in id_list:
        xmlfile = filepath + id +".xml"
        print("Parsing ", xmlfile)
        tweet_list = parseXML(xmlfile)
        data_train[id] = tweet_list
    return data_train


def parseXML(xmlfile): 
    tree = ET.parse(xmlfile) 
    root = tree.getroot()
    tweets = root[0]
    tweet_list = []
    for t in tweets:
        cdatatext = t.text
        tweet_list.append(cdatatext)
    return tweet_list


filename = "data/en/truth-train.txt"
truth_train = np.genfromtxt(filename, delimiter = ':::', dtype = 'U32')
data_train = readData(truth_train[:,0])
print(len(data_train), 'training examples')
print(len(data_train['754903b310327bbf56600ac33f205a81']), 'tweets in each example')


