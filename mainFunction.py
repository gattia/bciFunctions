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

examID = {}
allSegmentations={}
start = time.clock()

for index in range(len(listFiles)):
  filename = listFiles[index]
  examID[index] = str(re.sub('.npy', '', filename))
  allSegmentations[examID[index]] = (numpy.load(filename)).astype('int8')
  
#loop through and create distance maps



#for index in range(len(exam)):
tibia = {}
femur = {}
index = 0
print('iteration' + str(index))
image=examID[index]
labelMap = (allSegmentations[image]).astype(int)

#creat images of bones / cart / whole for tibia and femur
tibiaNormalizedDistanceMap, tibiaDistanceMap = createMapsFunction(labelMap, tibiaBoneLabel, tibiaCartLabel, transformationMatrix)

femurNormalizedDistanceMap, femurDistanceMap = createMapsFunction(labelMap, femurBoneLabel, femurCartLabel, transformationMatrix)

    
figure = plt.figure(figsize=(10,10))
plt.imshow(tibiaNormalizedDistanceMap[:,:,30], cmap='gray')
figure = plt.figure(figsize=(10,10))
plt.imshow(femurNormalizedDistanceMap[:,:,30], cmap='gray')

figure = plt.figure(figsize=(10,10))
plt.imshow(tibiaDistanceMap[:,:,30], cmap='gray')
figure = plt.figure(figsize=(10,10))
plt.imshow(femurDistanceMap[:,:,30], cmap='gray')

end = time.clock()
elapsed = str(end-start)
print('One loop took:' + elapsed + 'seconds')
numpySaveData(numpySave, image + '_femur.npy', femurNormalizedDistanceMap)
numpySaveData(numpySave, image + '_tibia.npy', tibiaNormalizedDistanceMap)
