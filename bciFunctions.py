''' 
Functions for normalized distance map creation
'''
import numpy
import os
from skimage.segmentation import find_boundaries
from scipy.spatial import distance
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
#from numba import jit
from scipy.spatial import distance

def numpySaveData (path, fileName, dataName):
  try: 
    numpy.save(path + fileName, dataName)
  except IOError:
    os.mkdir(path)
  numpy.save(path + fileName, dataName)

def importAndStorLabelImages(listFiles, imagesLocation):
  os.chdir(imagesLocation)
  listFiles = glob.glob('*.npy')
  for index in range(len(listFiles)):
    filename = listFiles[index]
    examID[index] = str(re.sub('.npy', '', filename))
    allSegmentations[examID[index]] = (numpy.load(filename)).astype('int8')
  return()

def createBinaryCartBoneMaps(labelMap, boneLabel, cartLabel):
  boneMap = numpy.zeros(shape=(labelMap.shape))
  boneMap[numpy.where(labelMap==boneLabel)] = 1
  cartMap = numpy.zeros(shape=(labelMap.shape))
  cartMap[numpy.where(labelMap==cartLabel)] = 2
  return(boneMap.astype('float32'), cartMap.astype('float32'))

def findBinaryMapBoundaries(boneMap, cartMap):
  # boneBoundary = find_boundaries(boneMap, mode = 'inner').astype(int) #this identifies points inside the bone (NOT cartilage)
#   cartBoundary = find_boundaries(cartMap).astype(int)# this creates a "double" boundary where there are two pixels thick, one inside and one outside of the cartilage.
#   adjacentBone = numpy.multiply(boneBoundary, cartBoundary) #by multiplying these we end up with only the ones that are "in" the bone but adjacent to cartialge.
#   bci = numpy.multiply
  
  boneBoundaryCart = find_boundaries(boneMap).astype('int') #here we identify  the bone (two pixels thick) - inside and outside. 
  cartBoundaryInner = find_boundaries(cartMap, mode = 'inner').astype('int') #Here we identify only the points that are "inside" the cartilage.... its definitely "cartilage"
  bciCart = numpy.multiply(boneBoundaryCart, cartBoundaryInner)# this gives us the "inside" of the bone/cartilage interface. I.e. points on the boundary that are inside of the cartilage.
  articularSurface = cartBoundaryInner - bciCart #take pizels that are labeled as being the inside of the cartilage and subtract the points on the inside that are adjacent to the bone. This leaves us with just the points that are inside the cartilage but are NOT adjacent to the bone.
  return(bciCart.astype('float32'), articularSurface.astype('float32'))

def getPointLocations (cartLabel, bci, articularSurface, transformation, labelMap):
  cartilagePoints = numpy.array(numpy.where(labelMap == cartLabel), dtype=('int'))
  bciPoints = numpy.array(numpy.where(bci ==1),dtype=('float32'))
  articularSurfacePoints = numpy.array(numpy.where(articularSurface ==1),dtype=('float32'))
  
  cartPointsRAS = (numpy.dot(transformation, cartilagePoints))
  bciPointsRAS = (numpy.dot(transformation, bciPoints))
  articularPointsRAS = (numpy.dot(transformation, articularSurfacePoints))
  
  normalizedDistanceMap = (numpy.zeros(shape=(labelMap.shape)))
  return(cartilagePoints, cartPointsRAS, bciPointsRAS, articularPointsRAS, normalizedDistanceMap)

# def makeDistanceMaps (cartilagePoints, cartPointsRAS, bciPointsRAS, articularPointsRAS, normalizedDistanceMap):
#   dBone = distance.cdist(numpy.transpose(cartPointsRAS), numpy.transpose(bciPointsRAS), 'euclidean').min(axis=1)
#   dSurface =distance.cdist(numpy.transpose(cartPointsRAS), numpy.transpose(articularPointsRAS), 'euclidean').min(axis=1)
#   totalDistance = dBone + dSurface
#   normDistance = dBone / totalDistance
#
#   distanceMap = (numpy.zeros(shape=(normalizedDistanceMap.shape))).astype('float32')
#   distanceMap[list(cartilagePoints)] = dBone
#   normalizedDistanceMap[list(cartilagePoints)] = normDistance
#
#   return(normalizedDistanceMap, distanceMap)

def makeDistanceCalculations (cartPointsRAS, bciPointsRAS, articularPointsRAS):
  dBone = distance.cdist(numpy.transpose(cartPointsRAS), numpy.transpose(bciPointsRAS), 'euclidean').min(axis=1)
  dSurface =distance.cdist(numpy.transpose(cartPointsRAS), numpy.transpose(articularPointsRAS), 'euclidean').min(axis=1)
  totalDistance = dBone + dSurface
  normDistance = dBone / totalDistance
  
  # distanceMap = (numpy.zeros(shape=(normalizedDistanceMap.shape))).astype('float32')
#   distanceMap[list(cartilagePoints)] = dBone
#   normalizedDistanceMap[list(cartilagePoints)] = normDistance
  
  return(normDistance)
  

def createMapsFunction (labelMap, boneLabel, cartLabel, transformation):
  boneMap, cartMap = createBinaryCartBoneMaps(labelMap, boneLabel, cartLabel)
  boneLabel = None
  bci, articularSurface = findBinaryMapBoundaries(boneMap, cartMap)
  boneMap = None; cartMap = None 
  cartilagePoints, cartPointsRAS, bciPointsRAS, articularPointsRAS, normalizedDistanceMap = getPointLocations (cartLabel, bci, articularSurface, transformation, labelMap)
  transformation = None; labelMap = None; articularSurface = None; bci = None; cartLabel = None
  #distanceMap = (numpy.zeros(shape=(normalizedDistanceMap.shape))).astype('float32')
  loops = 3
  section = numpy.floor(len(cartPointsRAS[1,:])/loops)
  for index in range(loops):
    print('loop' + str(index))
    if index < (loops-1):
      dataset = cartPointsRAS[:,(index*section):((index+1)*section)]
      normDistance = makeDistanceCalculations (dataset, bciPointsRAS, articularPointsRAS)
      dataPoints = cartilagePoints[:,(index*section):((index+1)*section)]
      normalizedDistanceMap[list(dataPoints)] = normDistance
    elif index ==(loops-1):
      dataset = cartPointsRAS[:,index*section:]
      #print('dataset')
      normDistance = makeDistanceCalculations (dataset, bciPointsRAS, articularPointsRAS) 
      #print('normDist')
      dataPoints = cartilagePoints[:,index*section:]
      #print('dataPoints')
      normalizedDistanceMap[list(dataPoints)] = normDistance  
      #print('Map')
  return(normalizedDistanceMap, cartilagePoints, dataPoints, dataset)