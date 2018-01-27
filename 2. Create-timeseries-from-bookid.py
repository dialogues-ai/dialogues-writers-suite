# -*- coding: utf-8 -*-

# 
#READ BOOK
# Create timesseries of books

from os import listdir
from os.path import isfile, join, isdir
from json import loads
from sys import path
import pandas as pd
from numpy import dot,cumsum,floor,zeros,sum,array,random,ones
from bookclass import Book_raw_data
from labMTsimple.speedy import LabMT
my_LabMT = LabMT()


book_ids = 1

#slides rawtext of books through labMT and gets timeseries
#gets matrix of matrixes a timeseries matrix for every bookselected
filteredbooks = [907]

#plays = [1787,1533,2263,2235,2253,1128,1777,1110,1118,1134]
timeseries = []
for book in filteredbooks:
    b = Book.objects.get(gutenberg_id=p)
    b_data = Book_raw_data(b)
    print(b.txt_file_path)
    try:
        b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=1.0,randomize=False,use_cache=True)
    except:
        print("couldn't find",b.title)
        pass
    # print(b_data.timeseries)
    timeseries.append(b_data.timeseries)
    
    
#Store timeseries matrix to as picle to be loaded and uploaded in other programs

big-time-series-matrix = timeseries
pickle.dump('big-time-series-matrix', 'rb')






#USE book_raw_data directory
#ORIGINAL working directory: /Users/home/Desktop/NN\ Projects/Emotional\ Arcs/core-stories 
os.chdir(os.path.join("/Volumes/NewVolume/books"))

#OPEN bookid txt from book_raw_data database
f = open('1.txt', 'r')
    
#READ bookid into library
book_raw_data = f.read()

#STORE bookid text in library
library = [book_raw_data]

