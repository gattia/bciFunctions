# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 13:31:37 2016

@author: gattia
"""
from scipy.spatial import distance

x = [[1,1,1], [2,2,2], [3,3,3], [4,4,4], [5,5,5]]
y = [[2,2,2], [3,3,3], [4,4,4], [5,5,5], [6,6,6]]

distance = distance.cdist(x,y,'euclidean')

d = numpy.sqrt((((x-y)**2).sum(axis=1)))

result = numpy.zeros(shape=(len(x)))
for i in range(len(x)):
  result[i] = numpy.sqrt((((x[0] - y[i])**2).sum()))
  
  
  

test = numpy.zeros(shape=(10,10,10))
locations = numpy.transpose([[1,1,1], [2,2,2], [3,3,3], [4,4,4], [5,5,5], [6,6,6], [7,7,7], [8,8,8]])
value = [1,2,3,4,5,6,7,8]

test[locations] = value


i = numpy.zeros(shape=(10,10))
loc = numpy.asarray([[1,2],[1,2]])
loc=list(loc)
i[loc] = numpy.asarray([2,3])