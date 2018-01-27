#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:05:00 2017

@author: home
"""

from os import listdir
from os.path import isfile, join
import sys
sys.path.append("/Volumes/NewVolume/Emotional-Arcs/tools")
from dogtoys import *
from json import loads
from re import findall,UNICODE
from labMTsimple.speedy import LabMT
my_LabMT = LabMT()
from labMTsimple.storyLab import *
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
#%matplotlib inline
from tools.bookclass import Book_raw_data
import pickle

import os
sys.path.append('/Volumes/NewVolume/Emotional-Arcs/database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gutenbergdb.settings')
import django
django.setup()

from tools.library.models import *

from datetime import datetime

use_cache = True



# all our essentials
from matplotlib import rc,rcParams
# rc('font', family='sans-serif') 
# rc('font', serif='Helvetica Neue')
# rc('text', usetex='false') 

rc('font', family='serif')
rc('font', family='cmr10')
rc('text', usetex='false') 

rcParams.update({'font.size': 12})
import matplotlib.pyplot as plt
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
#%matplotlib inline


## Filters books to use for analysis
q = Book.objects.filter(exclude=False,
                        length__gt=10000,
                        length__lte=200000,
                        downloads__gte=150,
                        numUniqWords__gt=1000,
                        numUniqWords__lt=18000,
                        lang_code_id=0).order_by("gutenberg_id")

## USES TIME-SERIES CACHE
## OR CREATES TIME-SERIES CACHE
books_failed = []
if isfile("/Volumes/NewVolume/Emotional-Arcs/database/cache/timeseries-matrix-cache-all.p") and use_cache:
    big_matrix = pickle.load(open("/Volumes/NewVolume/Emotional-Arcs/database/cache/timeseries-matrix-cache-all.p","rb"))
else:
    # load all of the timeseries into a matrix
    big_matrix = np.ones([len(q),200])
    # big_matrix_mean0 = np.ones(big_matrix.shape)
    stop_val = 1.0
    for i,b in enumerate(q):
        try:
            if i%100 == 0:
                print(i)
                # print(b.title)
            b_data = Book_raw_data(b)
            a = b_data.chopper_sliding(my_LabMT,num_points=200,stop_val=stop_val,randomize=False,use_cache=True)
            big_matrix[i,:] = b_data.timeseries
        except:
            books_failed.append(b.id)
            pass
    print(big_matrix.shape)
    pickle.dump(big_matrix,open("/Volumes/NewVolume/Emotional-Arcs/database/cache/timeseries-matrix-cache.p","wb"),pickle.HIGHEST_PROTOCOL)
    
big_matrix_mean0 = big_matrix-np.tile(big_matrix.mean(axis=1),(200,1)).transpose()
big_matrix_start0 = big_matrix-np.tile(big_matrix[:,0],(200,1)).transpose()
print(big_matrix.shape)

#pickle.dump(books_failed,open("/Volumes/NewVolume/Emotional-Arcs/database/saved-data/failed-books-dwl-100001-200000.p","wb"),pickle.HIGHEST_PROTOCOL)
    

# @andyreagan POTENTIALLY USEFUL

def mysub2ind(i,n,m):
    # convert the i-th index of a flattened n x m matrix
    # into the i,j of that matrix
    j = int(np.floor(i/float(m)))
    k = i-m*j
    return j,k

def myind2sub(j,k,n,m):
    # convert the [j,k]-th index of an n x m matrix
    # into the i of the flattened matrix
    i = j*n + k
    return int(i)

assert myind2sub(mysub2ind(20,15,15)[0],mysub2ind(20,15,15)[1],15,15) == 20



##
## THIS IS THE SOM MODEL
##  

# function [B,rmse_all] = train_SOM(A,B,C,numiter,randorder,scaling_fun,nbd_fun,iterstart)
def train_SOM(data,node_states,network_size,numiter,scaling_fun,nbd_fun,randorder=True,iterstart=0,returnDis=False):

    num_training_patterns = data.shape[0]
    print(num_training_patterns)
    num_nodes = node_states.shape[0]
    
    pairwise_distances = np.zeros([num_nodes,num_nodes])
    for i in range(num_nodes):
        for j in range(num_nodes):
            ind1 = mysub2ind(i,network_size[0],network_size[1])
            ind2 = mysub2ind(j,network_size[0],network_size[1])
            pairwise_distances[i,j] = np.abs(ind1[0]-ind2[0])+np.abs(ind1[1]-ind2[1])
    print("pairwise distance:")
    print(pairwise_distances[5,:])
    # plt.figure(figsize=(10,10))
    # plt.imshow(pairwise_distances)
    # plt.title('pairwise distance matrix')
    # mysavefig('SOM-5x5-distanceMatrix.png')
    # plt.show()

    rmse_avg = np.zeros(numiter)

    print('going for {0} iterations now'.format(numiter))
    for i in range(iterstart,numiter+iterstart):
        print('on training iteration no {0}'.format(i))
        order = np.arange(num_training_patterns)
        # order = np.arange(1)

        if randorder:
            np.random.shuffle(order)

        # go get the scaling parameter
        scaling_coeff = scaling_fun(i)
        print('scaling coeff is {0}'.format(scaling_coeff))
        
        # print(order)
        for j in order:
            # find the index of the winner
            #print(data[j,:])
            diff = node_states-data[j,:]
            dist = np.sqrt(np.sum(diff**2,axis=(1)))
            #print(dist)
            min_dist = dist.min()
            winning_node = dist.argmin()

#            print('winning node is {0}'.format(winning_node))
            rmse_avg[i-iterstart] += min_dist
            nbd,nbd_coeffs = nbd_fun(i,pairwise_distances[winning_node,:])
#            print('tuning the nbd of size {0}'.format(len(nbd)))
#            print(nbd)
            for n,a in zip(nbd,nbd_coeffs):
#                 print(n)
#                 print(a.shape)
#                 print(node_states[n,:])
#                 print(data[j,:].shape)
#                 print(node_states[n,:]-data[j,:])
#                 print(scaling_coeff)
#                 print(a)
                 node_states[n,:] = node_states[n,:] - scaling_coeff*a*(node_states[n,:]-data[j,:])
#                 print('after:')
#                 print(node_states[n,:])

    if returnDis:
        return node_states,rmse_avg,pairwise_distances
    else:
        return node_states,rmse_avg
    
    
##
## USE SOM ON BOOK DATA
##      
##

# start with 20x20
network_size = (13,13)
# network_size = (5,5)
num_nodes = network_size[0]*network_size[1]
node_states = np.random.randn(num_nodes,big_matrix.shape[1])*.05

# define some quick functions for the scalings
def scaling_fun_alpha(i,alpha):
    return np.power(i+1,alpha)

def nbd_fun_alpha(iteration,distance_list,alpha):
    tmp = np.arange(distance_list.shape[0])
    tmp2 = np.ones(distance_list.shape[0])
    max_d = np.sqrt(num_nodes)*np.power(iteration+1,alpha)
    # max_d = 3.0
    return tmp[distance_list < max_d],tmp2[distance_list < max_d]

iterations = 500
trained_nodes,rmse = train_SOM(big_matrix_mean0,
                               node_states,
                               network_size,
                               iterations,
                               lambda x: scaling_fun_alpha(x,-0.15),
                               lambda x,y: nbd_fun_alpha(x,y,-0.15))
    
print(trained_nodes)
print(rmse)


##
## PLOT LOSS
##

plt.figure(figsize=(10,10))
plt.plot(range(iterations),rmse)
plt.title('SOM RMSE')
# mysavefig('SOM-{0}x{0}-RMSE.png'.format(network_size[0]))


##
## PLOT WHICH NODES HAVE MOST COMMON TIME-SERIES 
##  (see which emotional-arcs are most common)

data = big_matrix
winning_node_list = np.zeros(data.shape[0])
for j in range(data.shape[0]):
    diff = trained_nodes-data[j,:]
    dist = np.sqrt(np.sum(diff**2,axis=(1)))
    winning_node_list[j] = dist.argmin()
plt.figure(figsize=(10,10))
n,bins,patches = plt.hist(winning_node_list,bins=num_nodes)
plt.title('SOM Winning Nodes')
# mysavefig('SOM-{0}x{0}-node-hist.png'.format(network_size[0]))



# now let's also plot them
def plot_clusters(clusters,data,cluster_centers,cluster_id,v=True,fix_ylim=True,xspacing=.01,investigate=False,save=True):
    # we are going to make plots of max width 3
    num_x = np.min([3,len(clusters)])
    num_y = np.ceil(len(clusters)/num_x)
    xspacing = .03
    yspacing = .03
    xoffset = .07
    yoffset = .07
    xwidth = (1.-xoffset)/(num_x)-xspacing
    yheight = (1.-yoffset)/(num_y)-yspacing
    print('xwidth is {0}'.format(xwidth))
    print('yheight is {0}'.format(yheight))
    
    # go compute the ybounds:
    calc_ylim = [100.0,-100.0]
    for cluster in clusters:
        c_max = data[cluster[0][:20],:].max()
        c_min = data[cluster[0][:20],:].min()
        calc_ylim[0] = np.min([calc_ylim[0],c_min])
        calc_ylim[1] = np.max([calc_ylim[1],c_max])
        
    chars = 60
    
    scale_factor_x = 5
    scale_factor_y = 5*1.25
    if investigate:
        scale_factor_x = 10
        scale_factor_y = 10*1.25
    fig = plt.figure(figsize=(scale_factor_x*num_x,scale_factor_y*num_y))
    for i,cluster in enumerate(clusters):
        print(i)
        print("====")
        # print((i-i%num_x))
        # ind = np.argsort(w[:,sv+svstart])[-20:]
        ax1rect = [xoffset+(i%num_x)*(xspacing+xwidth),1.-yheight-yspacing-(int(np.floor((i-i%num_x)/num_x))*(yspacing+yheight))+yheight*.2,xwidth,yheight*.8]
        ax1 = fig.add_axes(ax1rect)
        ax1books_rect = ax1rect.copy()
        ax1books_rect[1] -= yheight*.2
        ax1books_rect[3] = yheight*.2
        ax1books = fig.add_axes(ax1books_rect)
        # ax1books.text?
        # ax.set_title('20 closest positive correlates')
        
        if v:
            print('-'*80)
            print('20 closest positive correlates:')
            # print(cluster)
        j=0
        for index,title in zip(*cluster):
            if j+1 > 20:
                break
            if investigate:
                ax1.plot(data[index],label="{} ({})".format(title,q[int(index)].gutenberg_id))
            else:
                ax1.plot(data[index],color=".4",label=None)
            # plt.plot(big_matrix_mean0[i],color=".4")
            if v:
                print(index,title)
            if j<5:
                ax1books.text(0.0,.8-j*.2,"{} ({})".format(title,q[int(index)].gutenberg_id),fontsize=10)
            j+=1
        ax1.plot(cluster_centers[cluster_id[i]],color="#ff6700",linewidth=2,label="Node {} Cluster {} ({})".format(cluster_id[i],i+1,len(cluster[0])))
        # ax1.set_xticklabels([])
        ax1.legend(loc="upper right")

        # ax1.axis('off')
        ax1books.axis('off')
        
        props = dict(boxstyle='square', facecolor='white', alpha=1.0)
        # fig.text(ax1rect[0]+.03/xwidth, ax1rect[1]+ax1rect[3]-.03/yheight, letters[i],
        if fix_ylim:
            my_ylim = calc_ylim
        else:
            my_ylim = ax1.get_ylim()
        ax1.text(.035*200, my_ylim[0]+.965*(my_ylim[1]-my_ylim[0]), letters[i],
                     fontsize=14,
                     verticalalignment='top',
                     horizontalalignment='left',
                     bbox=props)

        if fix_ylim:
            ax1.set_ylim(calc_ylim)
        if fix_ylim and i%num_x > 0:
            ax1.set_yticklabels([])
        if True: # i<num_x*(num_y-1): # only on the bottom row
            ax1.set_xticklabels([])
            
    if save:
        # mysavefig('SV{0}.svg'.format('4-6'))
        mysavefig("clustered-timeseries.png".format(),
                  folder="media/figures/SOM",
                  openfig=False)
        mysavefig("clustered-timeseries.pdf".format(),
                  folder="media/figures/SOM",
                  openfig=True)

# let's look at what we have to build the data to plot. here are the trained nodes:

trained_nodes.shape

winning_node_list.shape
# looks like a list of the winning node for each story

winning_node_list[:10]
# peek at the winning nodes

n
# this is binned onto each node index by plt.hist() (count of wins by node)

len(n)
# make sure I have 100 bins
#andy's result was n = 169



# must have done a 10x10!
# let's rebuild n anyway
n_nodes = [np.nonzero(winning_node_list==i)[0] for i in range(num_nodes)]
print(n_nodes)
n = list(map(len,n_nodes))
print(n)


n_indexer = sorted(range(len(n)),key=lambda i: n[i],reverse=True)
# let's sort the winning nodes
print(n_indexer)


n_sorted = [n[n_i] for n_i in n_indexer]

n_sorted[:9]
# okay, now we have sorted counts

n_indexer[:9]
# and the sorted nodes

winning_node_list==n_indexer[0]
# these are the stories that match winning node 1

np.nonzero(winning_node_list==82)
# here are their indices

len(np.nonzero(winning_node_list==82)[0])
# and BOOM there are 59 of them

clusters = [get_sorted(n_nodes[n_i]) for n_i in n_indexer[:9]]
# clusters = []


##
## THIS PLOTS THE MONEY SHOT
## COMMON NODES, WITH EACH TIME-SERIES AT IT IS PLOTTED TOGETHER

plot_clusters(clusters,big_matrix_mean0,trained_nodes,n_indexer,v=False,fix_ylim=True,xspacing=.01,investigate=False,save=True)

##
## PLOTS LOSS AT ITERATION, SUCCESSFUL NODES ON HEATMAP 
## 

cityBlock(trained_nodes[n_indexer[1],:],trained_nodes[n_indexer[2],:])

##

rc('text', usetex='true') 

plt.figure(figsize=(5,5))
# fig = plt.subplot(1,3,1)
# ax = fig.add_axes([.2,.2,.7,.7])
# plt.figure(figsize=(10,10))
plt.plot(range(iterations),rmse,color=".4",label="RMSE",linewidth=1)
plt.xlabel("Training iteration")
plt.ylabel("RMSE")
# mysavefig('SOM-{0}x{0}-RMSE.png'.format(network_size[0]))



mysavefig("training.pdf",folder="media/figures/SOM/",openfig=True,)

# SEE HEAT MAP

plt.figure(figsize=(7,7))

plot_B_matrix(trained_nodes,network_size,cmap="Greys",d=cityBlock,shrink=.8)
for i in range(9):
    if i==0:
        color=".1"
    else:
        color=".1"
    plt.text(mysub2ind(n_indexer[i],network_size[0],network_size[0])[1],
             mysub2ind(n_indexer[i],network_size[0],network_size[0])[0],
             letters[i],
             ha="center",
             va="center",
             fontsize=12,
             color=color)
plt.xlabel("$N_i$")
plt.ylabel("$N_j$")

mysavefig("Bmatrix-labeled.pdf",folder="media/figures/SOM/",openfig=True,)

## ANOTHER HEAT MAP

plt.figure(figsize=(7,7))

plt.imshow(np.reshape(n,network_size), aspect=1, cmap=plt.get_cmap('Greys'), origin='lower', interpolation='nearest', ) #extent=(-0.25,network_size[0]-0.75,-0.25,network_size[1]-0.75))
plt.colorbar(shrink=.8)
plt.xlim()
for i in range(9):
    if i==0:
        color=".99"
    else:
        color=".99"
    plt.text(mysub2ind(n_indexer[i],network_size[0],network_size[0])[1],
             mysub2ind(n_indexer[i],network_size[0],network_size[0])[0],
             letters[i],
             ha="center",
             va="center",
             fontsize=12,
             color=color)
    
plt.xlabel("$N_i$")
plt.ylabel("$N_j$")


mysavefig("heatmap-labeled.pdf",folder="media/figures/SOM/",openfig=True,)

# ~/tools/shell/2015-08-kitchentabletools/pdftile.pl 1 2 0.48 3 0 l 8 "" "" 2016-03-11-15-13-Bmatrix-labeled.pdf "" 2016-03-11-15-14-heatmap-labeled.pdf SOM-matrices
# ~/tools/shell/2015-08-kitchentabletools/pdftile.pl 1 3 0.3 3 0 l 8 "" "" 2016-03-11-15-10-training.pdf "" 2016-03-11-15-13-Bmatrix-labeled.pdf "" 2016-03-11-15-14-heatmap-labeled.pdf SOM
