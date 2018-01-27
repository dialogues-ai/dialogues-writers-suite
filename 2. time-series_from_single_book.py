
# coding: utf-8

# Computes Emotional arc of a book not
# in the gutenberg index. The book must be
# in a .txt file, inserted into the book database
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

from tools.library.models import *
from tools.bookclass import *

from tqdm import tqdm


# In[2]:


# all our essentials
from matplotlib import rc,rcParams
rc('font', family='sans-serif') 
rc('font', serif='Helvetica Neue')
rc('text', usetex='false')

rc('font', family='serif')
rc('font', family='cmr10')
rc('text', usetex='false')
# this should accomplish the same thing
rcParams['text.usetex'] = False
rcParams['text.latex.preamble'] = r'\usepackage{hyperref}'
rcParams['text.latex.unicode'] = True

rcParams.update({'font.size': 12})
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

# import matplotlib
# matplotlib.use("pgf")
# pgf_with_custom_preamble = {
#     "text.usetex": True,
#     "text.latex.unicode": True,
#     "pgf.preamble": [
#         r"\usepackage{hyperref}"
#         ]
# }
# matplotlib.rcParams.update(pgf_with_custom_preamble)
# matplotlib.rcParams.update({'font.size': 12})
# from matplotlib import pyplot as plt


# In[4]:

# Assumes book is in book database with id tag
# Puts book into server, define its author, title, gutID, and length

# Set this number for the one you put in the database

bookindex = #######
title = ''

b = Book.objects.create(gutenberg_id=bookindex)
b = Book.objects.get(gutenberg_id=bookindex)
b.txt_file_path = 'database/books/' +str(b.gutenberg_id) + '.txt'

#write in title of book
b.title = str(title)
b.save()


#Sets books id

books = [bookindex]
timeseries = []


# In[5]:

#Runs time-series for books in list

for p in books:
    b = Book.objects.get(gutenberg_id=p)
    b_data = Book_raw_data(b)
    print(b.txt_file_path)
    try:
        b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=1.0,randomize=False,use_cache=True)
    except:
        print("couldn't find",b.title)
        pass
    print(b_data.timeseries)
    timeseries.append(b_data.timeseries)

# In[5]:

#Plots a graph of books

for i,t in enumerate(timeseries):
    if t is not None:
        plt.figure(figsize=(8,5))
        plt.plot(t,linewidth=1.5,color=".2")
        plt.ylabel(r"$h_{textrm{avg}}$")
        plt.xlabel("Narrative Time")
        b = Book.objects.get(gutenberg_id=books[i])
        plt.title(b.title)
        #Saves plot of books to chosen directory as .pdf and or .png
        plt.savefig("/Volumes/NewVolume/Emotional-Arcs/media/timeseries_arc/pdf/{}.pdf".format(books[i]),bbox_inches="tight")
        plt.savefig("/Volumes/NewVolume/Emotional-Arcs/media/timeseries_arc/png/{}.png".format(books[i]),bbox_inches="tight",dpi=600)

# In[ ]:




