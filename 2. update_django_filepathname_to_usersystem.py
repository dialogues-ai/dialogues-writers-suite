#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:52:48 2017

@author: home
"""

## Change file path of Book Class to my file path


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

from tools.library.models import *
from tools.bookclass import *

from tqdm import tqdm

import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

##
##

##
## Run this section
## Add whatever your directory is

play_files = os.listdir('database/books')
doesnotexist_count = 0
for i, p in enumerate(play_files):
    try:
        b = Book.objects.get(gutenberg_id=int(p.split('.')[0]))
        b.txt_file_path = 'database/books/' +str(b.gutenberg_id) + '.txt'
        b.save()
        print(i, '###', b.txt_file_path)
    except ObjectDoesNotExist:
        doesnotexist_count += 1
        print("DOES NOT EXIST" + p)
    
    

b = Book.objects.get(gutenberg_id=3332)

#change filepath name
b.txt_file_path = 'database/books/' +str(b.gutenberg_id) + '.txt'

b.txt_file_path
#Save new filepath name
b.save()


##TESTING open, read, and 
b = Book.objects.get(gutenberg_id=1787)
b_data = Book_raw_data(b)
text = b_data.load_all_combined()

