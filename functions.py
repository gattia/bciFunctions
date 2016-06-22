#create bone / cart / both images for each bone - inputs are original labelMap and the labels associated with cartilage and bone for the bone of interest. 
def createCartBoneMaps(labelMap, boneLabel, cartLabel):
  boneMap = numpy.zeros(shape=(labelMap.shape))
  boneMap[numpy.where(labelMap==boneLabel)] = 1
  cartMap = numpy.zeros(shape=(labelMaps.shape))
  cartMap[numpy.where(labelMap==cartLabel)] = 2
  wholeMap = boneMap + cartMap
  return(wholeMap, boneMap, cartMap)
  
#find boundaries for the bone and for the cartilage images. Return a bci and articular surface map
def findBoundaries(boneMap, cartMap):
  boneBoundary = find_boundaries(boneMap, mode = 'inner').astype(int)
  cartBoundary = find_boundaries(cartMap).astype(int)
  bci = numpy.multiply(boneBoundary, cartBoundary)
  
  boneBoundaryCart = find_boundaries(boneMap).astype(int)
  cartBoundaryCart = find_boundaries(cartMap, mode = 'inner').astype(int)
  bciCart = numpy.multiply(boneBoundaryCart, cartBoundaryCart)
  articularSurface = boneBoundaryCart - bciCart
  return(bci, articularSurface)
  
#get individual coordinates for cartilage and BCI and articular surface. Then transform these into the RAS space. Then, pre-allocate some maps. 
def getPoints (cartilageLabel, bci, articularSurface, transformation):
  cartilagePoints = numpy.array(numpy.where(labelMap == cartilageLabel))
  bciPoints = numpy.array(numpy.where(bci ==1))
  articularSurfacePoints = numpy.array(numpy.where(articularSurface ==1))
  
  cartPointsRAS = numpy.dot(transformation, cartilagePoints)
  bciPointsRAS = numpy.dot(transformation, cartilagePoints)
  articularPointsRAS = numpy.dot(transformation, articularSurfacePoints)
  
  normalizedDistanceMap = numpy.zeros(shape=(labelMap.shape))
  return(cartilagePoints, cartPointsRAS, bciPointsRAS, articularPointsRAS, normalizedDistanceMap,)
  
#below could potentially be optimized by doing some of the steps on a whole matrix, like the dBone & dArt steps...   
def normDistanceMap (cartilagePoints, bciPointsRAS, cartPointsRAS, articularPointsRAS, normalizedDistanceMap):
  for pixel in range(len(cartilagePoints[1,:])):
    dBone = numpy.sqrt(((numpy.transpose(bciPointsRAS)-cartPointsRAS[:,pixel])**2).sum(axis=1))m #this is just pythagorean theorem to get the distance. We have squared the distance in X and Y and Z. We then add up the squares, and take the square root to get the euclidean distance. 
    minDBone = dBone.min()
    minDistancesBone = numpy.zeros(len(cartilagePoints[1,:]))
    minDistancesBone[pixel] = minDBone
    
    dArt = numpy.sqrt(((numpy.transpost(articularPointsRAS) - cartPointsRAS[:,pixel])**2).sum(axis=1))
    minDArt = dArt.min()
    minDistancesArt = numpy.zeros(len(cartilagePoints[1,:]))
    minDistancesArt[pixel] = minDArt
    
    totalDistance = minDBone + minDArt
    normDistance = minDBone/totalDistance
    
    normalizedDistanceMap[cartilagePoints[:,pixel][0], cartilagePoints[:,pixel][1], cartilagePoints[:,pixel][2]] = normDistance
    
  return(normalizedDistanceMap)
  
import 


tibialCart = numpy.where(labelMap ==3)
femoralCart = numpy.where(labelMap ==1)
tibia = numpy.where(labelMap ==4)
femur = numpy.where(labelMap ==5)

tibiaBoneMap = numpy.zeros(shape=(labelMap.shape))
tibiaBoneMap[tibia] = 4
tibiaCartMap = numpy.zeros(shape=(labelMap.shape))
tibiaCartMap[tibialCart] = 3
tibiaMap = tibiaBoneMap + tibiaCartMap

femurBoneMap = numpy.zeros(shape=(labelMap.shape))
femurBoneMap[femur] = 5
femurCartMap = numpy.zeros(shape=(labelMap.shape))
femurCartMap[femoralCart] = 1
femurMap = femurBoneMap + femurCartMap



''' 
PLAYING TO LOOK AT THE IMAGES WITH MATH... 
'''
tibiaNormalizedDistanceMap = numpy.zeros(shape=(tibiaNormalizedDistanceMap.shape))

for pixel in range(len(tibiaCartilagePoints[1,:])):
  dBone = numpy.sqrt(((numpy.transpose(tibiaBciPointsRAS)-tibiaCartPointsRAS[:,pixel])**2).sum(axis=1)) #this is just pythagorean theorem to get the distance. We have squared the distance in X and Y and Z. We then add up the squares, and take the square root to get the euclidean distance. 
  minDBone = dBone.min()
  minDistancesBone = numpy.zeros(len(tibiaCartilagePoints[1,:]))
  minDistancesBone[pixel] = minDBone
  
  dArt = numpy.sqrt(((numpy.transpose(tibiaArticularPointsRAS) - tibiaCartPointsRAS[:,pixel])**2).sum(axis=1))
  minDArt = dArt.min()
  minDistancesArt = numpy.zeros(len(tibiaCartilagePoints[1,:]))
  minDistancesArt[pixel] = minDArt
  
  totalDistance = minDBone + minDArt
  normDistance = minDBone/totalDistance
  
  tibiaNormalizedDistanceMap[tibiaCartilagePoints[:,pixel][0], tibiaCartilagePoints[:,pixel][1], tibiaCartilagePoints[:,pixel][2]] = normDistance