#Art of War
# /Users/home/mirrors.xmission.com/gutenberg/1/3/132

from os import listdir
from os.path import isfile, join
from json import loads
from re import findall,UNICODE
import sys
sys.path.append("/Users/home/Desktop/tools/Python")
from tools.dogtoys import *
from labMTsimple.speedy import LabMT
my_LabMT = LabMT()
from labMTsimple.storyLab import *
import numpy as np
from tools.bookclass import Book_raw_data
import pickle

import os
sys.path.append('/Volumes/NewVolume/Emotional Arcs/database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gutenbergdb.settings')
import django
django.setup()

from tools.library.models import *


# all our essentials
from matplotlib import rc,rcParams
# rc('font', family='sans-serif') 
# rc('font', serif='Helvetica Neue')
# rc('text', usetex='false') 


rc('font', family='serif')
rc('font', family='cmr10')
rc('text', usetex='true') 

rcParams.update({'font.size': 12})
import matplotlib.pyplot as plt
%matplotlib notebook
%matplotlib nbagg

from IPython.core.display import HTML
from IPython.display import display

q = Book.objects.filter(title="The Art of War")

q

plt.figure(figsize=(15,7.5))
for i,b in enumerate(q):
    print(b.title)
    for a in b.authors.all():
        print(a)
    print(b.exclude)
    print(b.excludeReason)
    print(b.gutenberg_id)
    HTML("http://www.gutenberg.org/ebooks/{0}/".format(b.gutenberg_id))
    if not b.exclude:
        b_data = Book_raw_data(b)
        a = b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=1.0)
        plt.subplot(2,2,i+1)
        plt.plot(b_data.timeseries)
        plt.title("{0} ({1})".format(b.title,b.gutenberg_id))



##
        
for b in q:
    HTML("<a href=\"http://www.gutenberg.org/ebooks/{0}/\">book link</a>".format(b.gutenberg_id))
    
##    

HTML("<a href=\"http://www.gutenberg.org/ebooks/{0}\" target=\"_blank\">book link</a>".format(q[0].gutenberg_id))

HTML("<a href=\"http://www.gutenberg.org/ebooks/{0}\" target=\"_blank\">book link</a>".format(q[1].gutenberg_id))

HTML("<a href=\"http://www.gutenberg.org/ebooks/{0}\" target=\"_blank\">book link</a>".format(q[2].gutenberg_id))

HTML("<a href=\"http://www.gutenberg.org/ebooks/{0}\" target=\"_blank\">book link</a>".format(q[3].gutenberg_id))


##
##
##

for b in q:
    b.exclude = True
    b.save()
    

q = Book.objects.filter(title__icontains="Romeo",exclude=False,language="en")

print(q)

for b in q:
    print(b.gutenberg_id,b.title,b.language)
    
    
##
## Plot
##    

fig = plt.figure(figsize=(15,7.5))
ax = fig.add_axes([.2,.2,.7,.7])
for b in q:
     b_data = Book_raw_data(b)
     a = b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=1.0)
     ax.plot(b_data.timeseries,label="{1} ({0})".format(b.gutenberg_id,b.title))
ax.legend()
    

##
## PLOT
##

fig = plt.figure(figsize=(15,7.5))
ax = fig.add_axes([.2,.2,.7,.7])
for b in q:
     b_data = Book_raw_data(b)
     a = b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=2.0)
     ax.plot(b_data.timeseries,label="{1} ({0})".format(b.gutenberg_id,b.title))
ax.legend()


##
##
##

b = Book.objects.get(gutenberg_id=47960)
b.exclude = True
b.excludeReason = "Annotated"
b.save()

for gid in [1112,1513,2261]:
    b = Book.objects.get(gutenberg_id=gid)
    b.exclude = True
    b.excludeReason = "Duplicate"
    b.save()
    

q = Book.objects.filter(gutenberg_id=19002)


fig = plt.figure(figsize=(15,7.5))
ax = fig.add_axes([.2,.2,.7,.7])
for b in q:
    b_data = Book_raw_data(b)
    a = b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=2.0)
    ax.plot(b_data.timeseries,label="{1} ({0})".format(b.gutenberg_id,b.title))
ax.legend()



##
##
##

for gid in [22657,17150,14403,1150,25880,19118,38877,28696,51207,]:
    b = Book.objects.get(gutenberg_id=gid)
    b.exclude = True
    b.excludeReason = "Non fiction"
    b.save()
    

for gid in [51205,33900,19116,38658,31630,28553,22577]:
    b = Book.objects.get(gutenberg_id=gid)
    b.exclude = True
    b.excludeReason = "Non fiction"
    b.save()
for gid in [22566,]:
    b = Book.objects.get(gutenberg_id=gid)
    b.exclude = True
    b.excludeReason = "Duplicate"
    b.save()
    
    
    
q = Book.objects.filter(title__icontains="pivot")
print(q)
    