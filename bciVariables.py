'''
Names / Lists / Variables 
'''
import datetime
import numpy

numpySegLocations = '/Users/gattia/Documents/researchProjects/cartilageDepthAnalysis/slicerData/numpySegmentations/'
dataStorageLocation = '/Users/gattia/Documents/Data/T2studies/Depth/'
date = datetime.date.today().isoformat()
folder = 'savedFiles_' + date

# if len(glob.glob(dataStorageLocation + folder)) ==0:
#   os.mkdir(dataStorageLocation + folder)
# numpySave = dataStorageLocation + folder + '/normDistanceMaps/'

# cartilage ROIs
femurCartLabel = 1
patellaCartLabel = 2
tibiaCartLabel = 3
tibiaBoneLabel = 4
femurBoneLabel= 5
patellaBoneLabel = 6

transformationMatrix = numpy.asarray([[0.3125, 0, 0], [0,0.3125,0], [0,0,1]], dtype=('float32'))

