#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:13:40 2017

@author: home
"""

## Things we need
##


from os import listdir, mkdir
from os.path import isfile, join, isdir
from json import loads
from re import findall,UNICODE
import sys
sys.path.append("/Volumes/NewVolume/Emotional Arcs/tools")
from dogtoys import *
from labMTsimple.speedy import LabMT
my_LabMT = LabMT()
from labMTsimple.storyLab import *
import numpy as np
import pickle

import os
sys.path.append('/Volumes/NewVolume/Emotional Arcs/database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gutenbergdb.settings')
import django
django.setup()

from tools.library.models import *
from tools.bookclass import *

from tqdm import tqdm

## Import 1 book

books = [1787,1533,2263,2235,2253,1128,1777,1110,1118,1134]

for book in books:
    b = Book.objects.get(gutenberg_id=book)
    b_data = Book_raw_data(b)
    print("Title: " + str(b.title))
    print("File Location: " + str(b.txt_file_path))
    print("Language: " + str(b.lang_code_id))
    print("Authors: " + str(b.authors))
    print("Word Count: " + str(b.length))
    print("Num of Downloads: " + str(b.downloads))
    print(" ")





