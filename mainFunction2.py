# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 21:31:08 2016

@author: gattia
"""
from bciVariables import *
from bciFunctions import *
import glob
import re
import numpy
import time


#make folder to save data in. 
if len(glob.glob(dataStorageLocation + folder)) ==0:
  os.mkdir(dataStorageLocation + folder)
numpySave = dataStorageLocation + folder + '/normDistanceMaps/'

#gather all of the segmentations & store together
os.chdir(numpySegLocations)
listFiles = glob.glob('*.npy')

#examID = {}
#allSegmentations={}


for index in range(len(listFiles)): #for index in range(len(listFiles))
  #loop through to load data and to create distance maps This should only hold one map in memory at a time and reduce memory... which I think was the major limit to this code before. 
  start = time.clock()
  tibia = {}
  femur = {}
  print('iteration' + str(index))
  filename = listFiles[index]
  image = str(re.sub('.npy', '', filename))
  labelMap = (numpy.load(filename)).astype('int8')
  
  
  
  
  #for index in range(len(exam)):
  
  
  #creat images of bones / cart / whole for tibia and femur
  tibiaNormalizedDistanceMap, cartilagePoints, dataPoints, dataset = createMapsFunction(labelMap, tibiaBoneLabel, tibiaCartLabel, transformationMatrix)
  end = time.clock()
  elapsed = str(end-start)
  #print('tibiaDone' + str(elapsed))
  
  femurNormalizedDistanceMap, cartilagePoints, dataPoints, dataset = createMapsFunction(labelMap, femurBoneLabel, femurCartLabel, transformationMatrix)
  end = time.clock()
  elapsed = str(end-start)
  #print('femurDone' + str(elapsed))
  
      
#  figure = plt.figure(figsize=(10,10))
#  plt.imshow(tibiaNormalizedDistanceMap[:,:,30], cmap='gray')
#  figure = plt.figure(figsize=(10,10))
#  plt.imshow(femurNormalizedDistanceMap[:,:,30], cmap='gray')
  
  end = time.clock()
  elapsed = str(end-start)
  print('Loop took:' + elapsed + ' seconds')
  numpySaveData(numpySave, image + '_femur.npy', femurNormalizedDistanceMap)
  numpySaveData(numpySave, image + '_tibia.npy', tibiaNormalizedDistanceMap)
