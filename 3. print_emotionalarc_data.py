
# coding: utf-8

# Print a .csv of all emotional arc data
# includes: timeseries, title, gut_id, downloads, length
# 
# ----------------------------------------------
# 
# 

from os import listdir, mkdir
from os.path import isfile, join, isdir
from json import loads
from re import findall,UNICODE
import sys
sys.path.append("/Volumes/NewVolume/Emotional-Arcs/tools")
from dogtoys import *
from labMTsimple.speedy import LabMT
my_LabMT = LabMT()
from labMTsimple.storyLab import *
import numpy as np
import pickle

import os
sys.path.append('/Volumes/NewVolume/Emotional-Arcs/database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gutenbergdb.settings')
import django
django.setup()
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from tools.library.models import *
from tools.bookclass import *

from tqdm import tqdm

# In[4]:



## Filters books to use for analysis
q = Book.objects.filter(exclude=False,
                        length__gt=20000,
                        length__lte=200000,
                        downloads__gte=75,
                        numUniqWords__gt=1000,
                        numUniqWords__lt=18000,
                        lang_code_id=0,).order_by("gutenberg_id")


## OR PICK INDIVIDUAL BOOK
#
#plays = [1787,1533,2263,2235,2253,1128,1777,1110,1118,1134]
#timeseries = []
#
#for p in plays:
#    b = Book.objects.get(gutenberg_id=p)
#    a = Author.objects.get(gutenberg_id=p)
#    b_data = Book_raw_data(b)
#    print(b.txt_file_path)
#    try:
#        b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=1.0,randomize=False,use_cache=True)
#    except:
#        print("couldn't find",b.title)
#        pass
#    print(b_data.timeseries)
#    timeseries.append(b_data.timeseries)



## 

big_matrix = np.ones([len(q), 200 + 4])

titles = []
authors = []
language = []
failed_files = []

# In[5]:

for i,b in enumerate(q):
    try:
        b_data = Book_raw_data(b)
        a = b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=1.0,randomize=False,use_cache=True)
    except (FileNotFoundError, OSError):
        failed_files.append(b.gutenberg_id)
    #integer data
    big_matrix[i,0] = b.gutenberg_id
    big_matrix[i,1] = b.length
    big_matrix[i,2] = b.numUniqWords
    big_matrix[i,3] = b.downloads
    big_matrix[i,4:204] = b_data.timeseries
    
    #str data
    c = b.authors.all()
    authors.append(c)
    titles.append(b.title)
    language.append(b.language)

#authors = []
#for b in enumerate(q[:10]):
#    b_data = Book_raw_data(b)
#    print(b.gutenberg_id)
#    a = Authors.objects.get(gutenberg_id = b.gutenberg_id)
#    authors.append(c.fullname)
    
    

print(big_matrix.shape)
    

#SAVES INTO .CSV

import csv

## Export timeseries
with open("emotional-arc_data.csv", "w") as t:
    writer = csv.writer(t)
    writer.writerows(big_matrix)

## Export Titles
with open("emotional-arc_data_titles.csv", "w") as f:
    writer = csv.writer(f)
    for title in titles:
        writer.writerow([title])

## Export Authors
with open("emotional-arc_data_authors.csv", "w") as f:
    writer = csv.writer(f)
    for author in authors:
        writer.writerow([author])




