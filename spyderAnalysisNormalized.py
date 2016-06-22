# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:21:36 2016

@author: gattia
"""
import numpy
import os
import skimage
from skimage.segmentation import find_boundaries
from skimage.segmentation import mark_boundaries
import scipy
from scipy.spatial import distance
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import glob
import re
import datetime
#from numba import jit
from scipy.spatial import distance

def closest_node(node, nodes):
    nodes = numpy.asarray(nodes)
    dist_2 = numpy.sum((nodes - node)**2, axis=1)
    return numpy.argmin(dist_2)

def closest_point(pt, others):
  distances = cdist(pt, others)
  return others[distances.argmin()]
  
def numpySaveData (path, fileName, dataName):
  try: 
    numpy.save(path + fileName, dataName)
  except IOError:
    os.mkdir(path)
  numpy.save(path + fileName, dataName)
  
  
numpySegLocations = '/Users/gattia/Documents/researchProjects/cartilageDepthAnalysis/slicerData/numpySegmentations/'
dataStorageLocation = '/Users/gattia/Documents/Data/T2studies/Depth/'
date = datetime.date.today().isoformat()
folder = 'savedFiles_' + date
if len(glob.glob(dataStorageLocation + folder)) ==0:
  os.mkdir(dataStorageLocation + folder)

numpySave = dataStorageLocation + folder + '/normDistanceMaps/'

os.chdir(numpySegLocations)
listFiles = glob.glob('*.npy')

examID = {}
allSegmentations={}

for index in range(len(listFiles)):
  filename = listFiles[index]
  examID[index] = str(re.sub('.npy', '', filename))
  allSegmentations[examID[index]] = numpy.load(filename)
  
#labelMap = numpy.load('3655_Result.npy')

#femoral cart = 1
#patellar cart = 2
# tibial cart = 3
#tibia = 4
#femur= 5
#patella = 6

transformationMatrix = [[0.3125, 0, 0], [0,0.3125,0], [0,0,1]]

'''
BCI Functions and loops
'''
def createCartBoneMaps(labelMap, boneLabel, cartLabel):
  boneMap = (numpy.zeros(shape=(labelMap.shape)))[numpy.where(labelMap==boneLabel)] = 1
  cartMap = (numpy.zeros(shape=(labelMap.shape)))[numpy.where(labelMap==cartLabel)] = 2
  wholeMap = boneMap + cartMap
  return(boneMap.astype('float32'), cartMap.astype('float32'))
  
#find boundaries for the bone and for the cartilage images. Return a bci and articular surface map
def findBoundaries(boneMap, cartMap):
  boneBoundary = find_boundaries(boneMap, mode = 'inner')#.astype(int)
  cartBoundary = find_boundaries(cartMap).astype(int)
  bci = numpy.multiply(boneBoundary, cartBoundary)
  
  boneBoundaryCart = find_boundaries(boneMap).astype(int)
  cartBoundaryCart = find_boundaries(cartMap, mode = 'inner').astype(int)
  bciCart = numpy.multiply(boneBoundaryCart, cartBoundaryCart)
  articularSurface = boneBoundaryCart = bciCart
  return(bci.astype('float32'), articularSurface.astype('float32'))

#get individual coordinates for cartilage and BCI and articular surface. Then transform these into the RAS space. Then, pre-allocate some maps. 
def getPoints (cartilageLabel, bci, articularSurface, transformation):
  cartilagePoints = numpy.array(numpy.where(labelMap == cartilageLabel), dtype=('float32'))
  bciPoints = numpy.array(numpy.where(bci ==1),dtype=('float32'))
  articularSurfacePoints = numpy.array(numpy.where(articularSurface ==1),dtype=('float32'))
  
  cartPointsRAS = (numpy.dot(transformation, cartilagePoints)).astype('float32')
  bciPointsRAS = (numpy.dot(transformation, bciPoints)).astype('float32')
  articularPointsRAS = (numpy.dot(transformation, articularSurfacePoints)).astype('float32')
  
  normalizedDistanceMap = (numpy.zeros(shape=(labelMap.shape))).astype('float32')
  return(cartilagePoints, cartPointsRAS, bciPointsRAS, articularPointsRAS, normalizedDistanceMap)

#@jit(['float64(int64, float64, float64, float64, float64)'], target = 'cpu')
#def normDistanceMap (cartilagePoints, bciPointsRAS, cartPointsRAS, articularPointsRAS, normalizedDistanceMap):
#  distanceMap = numpy.zeros(shape=(normalizedDistanceMap.shape))
#  for pixel in range(len(cartilagePoints[1,:])):
#    dBone = numpy.sqrt(((numpy.transpose(bciPointsRAS)-cartPointsRAS[:,pixel])**2).sum(axis=1)) #this is just pythagorean theorem to get the distance. We have squared the distance in X and Y and Z. We then add up the squares, and take the square root to get the euclidean distance. 
#    minDBone = dBone.min()
#    minDistancesBone = numpy.zeros(len(cartilagePoints[1,:]))
#    minDistancesBone[pixel] = minDBone
#    
#    dArt = numpy.sqrt(((numpy.transpose(articularPointsRAS) - cartPointsRAS[:,pixel])**2).sum(axis=1))
#    minDArt = dArt.min()
#    minDistancesArt = numpy.zeros(len(cartilagePoints[1,:]))
#    minDistancesArt[pixel] = minDArt
#    
#    totalDistance = minDBone + minDArt
#    normDistance = minDBone/totalDistance
#    
#    normalizedDistanceMap[cartilagePoints[:,pixel][0], cartilagePoints[:,pixel][1], cartilagePoints[:,pixel][2]] = normDistance
#    
#    distanceMap[cartilagePoints[:,pixel][0], cartilagePoints[:,pixel][1], cartilagePoints[:,pixel][2]] = minDBone
#  return(normalizedDistanceMap, distanceMap)
#  

def normDistanceMap (cartilagePoints, bciPointsRAS, cartPointsRAS, articularPointsRAS, normalizedDistanceMap):
  dBone = distance.cdist(numpy.transpose(cartPointsRAS), numpy.transpose(bciPointsRAS), 'euclidean').min(axis=1)
  dSurface =distance.cdist(numpy.transpose(cartPointsRAS), numpy.transpose(articularPointsRAS), 'euclidean').min(axis=1)
  totalDistance = dBone + dSurface
  normDistance = dBone / totalDistance
  
  distanceMap = (numpy.zeros(shape=(normalizedDistanceMap.shape))).astype('float32')
  distanceMap[list(cartilagePoints)] = dBone
  normalizedDistanceMap[list(cartilagePoints)] = normDistance
  
  return(normalizedDistanceMap, distanceMap)
  

femurCartLabel = 1
patellaCartLabel = 2
tibiaCartLabel = 3
tibiaBoneLabel = 4
femurBoneLabel= 5
patellaBoneLabel = 6

print('starting loop')
#for index in range(len(exam)):
tibia = {}
femur = {}
index = 0
print('iteration' + str(index))
image=examID[index]
labelMap = allSegmentations[image]

#creat images of bones / cart / whole for tibia and femur
tibiaWholeMap, tibiaBoneMap, tibiaCartMap = createCartBoneMaps(labelMap, tibiaBoneLabel, tibiaCartLabel)

femurWholeMap, femurBoneMap, femurCartMap = createCartBoneMaps(labelMap, femurBoneLabel, femurCartLabel)

tibiaBCI, tibiaSurface = findBoundaries(tibiaBoneMap, tibiaCartMap)
femurBCI, femurSurface = findBoundaries(femurBoneMap, femurCartMap)

tibiaCartilagePoints, tibiaCartPointsRAS, tibiaBciPointsRAS, tibiaArticularPointsRAS, tibiaNormalizedDistanceMap = getPoints(tibiaCartLabel, tibiaBCI, tibiaSurface, transformationMatrix)

femurCartilagePoints, femurCartPointsRAS, femurBciPointsRAS, femurArticularPointsRAS, femurNormalizedDistanceMap = getPoints(femurCartLabel, femurBCI, femurSurface, transformationMatrix)



print('starting distance map')
tibiaNormalizedDistanceMap, tibiaDistanceMap = normDistanceMap(tibiaCartilagePoints, tibiaBciPointsRAS, tibiaCartPointsRAS, tibiaArticularPointsRAS, tibiaNormalizedDistanceMap)

femurNormalizedDistanceMap, femurDistanceMap = normDistanceMap(femurCartilagePoints, femurBciPointsRAS, femurCartPointsRAS, femurArticularPointsRAS, femurNormalizedDistanceMap)
    
figure = plt.figure(figsize=(10,10))
plt.imshow(tibiaNormalizedDistanceMap[:,:,30], cmap='gray')
figure = plt.figure(figsize=(10,10))
plt.imshow(femurNormalizedDistanceMap[:,:,30], cmap='gray')

#  figure = plt.figure(figsize=(10,10))
#  plt.imshow(tibiaDistanceMap[:,:,30], cmap='gray')
#  figure = plt.figure(figsize=(10,10))
#  plt.imshow(femurDistanceMap[:,:,30], cmap='gray')
#  
#  os.chdir(numpySave)
#  numpy.save(image + '.npy', normalizedDistanceMap)
numpySaveData(numpySave, image + '_femur.npy', femurNormalizedDistanceMap)
numpySaveData(numpySave, image + '_tibia.npy', tibiaNormalizedDistanceMap)



#figure5 = plt.figure(figsize=(10,10))
#plt.imshow(x[:,:,20], cmap='gray')
  
fig = plt.figure()
display = plt.imshow(image[:,:,30])
fig.colorbar(display)

fig, ax = plt.subplots()
im = ax.imshow(image[:,:,30])
fig.colorbar(image[:,:,30], ax=ax)

##################### BELOW ARE IMAGES TO PLAY AND FIGURE OUT THE ORIENTATION############
#figure1 = plt.figure(1)
#plt.imshow(labelMap[:,:,30])
#
#figure2 = plt.figure(2)
#plt.imshow(tibiaCartBoundary[:,:,30])
#
#figure3 = plt.figure(figsize = (10,10))
#plt.imshow(bci[:,:,30], cmap = 'gray')
#transform2D = [[0.3125,0], [0,0.3125]]
#
#tibia30 = numpy.where(labelMap[:,:,30]==4)
#tibia30PointsTransformed = numpy.dot(transform2D, tibia30)
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(tibia30PointsTransformed[0,:], tibia30PointsTransformed[1,:], 'o', markersize=1, color='green', alpha=1)
#plt.axes().set_aspect('equal', 'datalim')
#
#tibiaPoints = numpy.dot(transformationMatrix, tibia)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(tibiaPoints[0,:], tibiaPoints[2,:], 'o', markersize=1, color='green', alpha=1)
#plt.axes().set_aspect('equal', 'datalim')
#
## THESE ARE TO SHOW THAT THE DIMENSIONS ARE CORRECT... 
#femurPoints = numpy.dot(transformationMatrix,femur)
#
#femur = numpy.where(labelMap == 5)
#
## Two subplots, the axes array is 1-d
#f, axarr = plt.subplots(3,2, figsize=(10,10), sharex = True, sharey = True)
#axarr[0,0].plot(femurPoints[2,:], femurPoints[1,:], 'o', markersize=1)
#axarr[0,0].set_title('Sharing X axis')
#axarr[0,1].plot(femurPoints[2,:], femurPoints[0,:], 'o', markersize=1)
#axarr[1,0].plot(femurPoints[1,:], femurPoints[0,:], 'o', markersize=1)
#axarr[1,1].plot(femurPoints[1,:], femurPoints[2,:], 'o', markersize=1)
#axarr[2,1].plot(femurPoints[1,:], femurPoints[0,:], 'o', markersize=1)
#plt.gca().set_aspect('equal')
#plt.draw()
#
##[0,:] & [1,:] is saggital 
##0,: & 2,:  is frontal 
##1,: & 2,: is axial. 