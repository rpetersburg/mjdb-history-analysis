import json
import couchdb
from datetime import datetime
from matplotlib import dates

class DBController():

    def __init__(self):
        pass
##        self.couchURL = 'http://feresa.physics.unc.edu:5984/'
##        self.couch = couchdb.Server( self.couchURL )
##        self.db = self.couch['history_mjdscm']


    def getParticleData( self, particleSize ):
        try:
            print 'Attempting to Load Particle Data'
            dataArray = self.loadParticleData( particleSize )
            print 'Load Successful'
        except IOError:
            print 'Particle Data does not exist. Gathering and Saving Records'
            self.saveParticleDataFromDatabase( particleSize )
            dataArray = self.loadParticleData( particleSize )
        return dataArray

    def saveParticleDataFromDatabase( self, particleSize ):
        print 'Getting ' + particleSize + ' um data from database'
        with open('database.json', 'r') as database:
            particleData = []
            n = 1
            for rec in database:
                if n % 10000 == 0:
                    print n ,
                if rec[0] in '[]':
                    continue
                try:
                    recDict = json.loads(rec[0:-2])
                    if recDict['id'][0] == '_':
                        continue
                    stringName = 'DR ' + str(particleSize) + ' um count'
                    for item in recDict['doc']['adcs']:
                        if stringName in item.keys():
                            particleData.append( {'count': item[stringName],
                                              'time': recDict['doc']['time'] } )
                except KeyError:
                    pass
                except ValueError:
                    print rec
                n += 1
            self.saveParticleData(particleData, particleSize)
            
    def getParticleCount( self, particleRec, particleSize ):
        adcsList = particleRec['doc']['adcs']
        stringName = 'DR ' + str(particleSize) + ' um count'
        if stringName in adcsList:
            return {'count': adcsList[adcsList.index(stringName)][stringName],
                    'time': particleRec['doc']['time'] }

    def saveParticleData( self, dataArray, particleSize ):
        with open('particleData' + str(particleSize) + '.json', 'w') as fp:
            json.dump(dataArray, fp)

    def loadParticleData( self, particleSize ):
        with open('particleData' + str(particleSize) + '.json', 'r') as fp:
            return json.load(fp)

    def copyDatabase( self ):
        #Use following in command prompt. Not sure how to implement in Python
        #curl -X GET http://feresa.physics.unc.edu:5984/history_mjdscm/_all_docs?include_docs=true > database.txt
        pass
