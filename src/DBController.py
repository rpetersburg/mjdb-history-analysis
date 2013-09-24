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


    def getParticleData( self, particleSize, room ):
        try:
            print 'Attempting to Load ' + room + ' ' + particleSize + ' um Particle Data'
            dataArray = self.loadParticleData( particleSize, room )
            print 'Load Successful\n'
        except IOError:
            print 'Particle Data does not exist. Gathering and Saving Records'
            self.saveParticleDataFromDatabase( particleSize, room )
            dataArray = self.loadParticleData( particleSize, room )
        return dataArray

    def saveParticleDataFromDatabase( self, particleSize, room ):
        print '\nGetting ' + room + ' ' + particleSize + ' um data from database'
        with open('database.json', 'r') as database:
            particleData = []
            n = 1
            for rec in database:
                if n % 100 == 0:
                    print 'Number of documents processed: ' + str(n) + '         \r',
                if rec[0] in '[]' or rec[-2] in '[]':
                    continue
                try:
                    recDict = json.loads(rec[0:-2])
                    if recDict['id'][0] == '_':
                        continue
                    stringName = room + ' ' + particleSize + ' um count'
                    for item in recDict['doc']['adcs']:
                        if stringName in item.keys():
                            particleData.append( {'count': item[stringName],
                                              'time': recDict['doc']['time'] } )
                except KeyError:
                    pass
                except ValueError:
                    recDict = json.loads(rec[0:-1])
                    if recDict['id'][0] == '_':
                        continue
                    stringName = room + '' + str(particleSize) + ' um count'
                    for item in recDict['doc']['adcs']:
                        if stringName in item.keys():
                            particleData.append( { 'count': item[stringName],
                                                   'time': recDict['doc']['time'] } )
                n += 1
            self.saveParticleData(particleData, particleSize, room)
            
    def getParticleCount( self, particleRec, particleSize, room ):
        adcsList = particleRec['doc']['adcs']
        stringName = room + '' + str(particleSize) + ' um count'
        if stringName in adcsList:
            return {'count': adcsList[adcsList.index(stringName)][stringName],
                    'time': particleRec['doc']['time'] }

    def saveParticleData( self, dataArray, particleSize, room ):
        print 'Saving ' + room + ' ' + particleSize + ' um data to file'
        with open( room + particleSize + 'particleData.json', 'w') as fp:
            json.dump(dataArray, fp)

    def loadParticleData( self, particleSize, room ):
        with open( room + particleSize + 'particleData.json', 'r') as fp:
            return json.load(fp)

    def saveAvgBaseData( self, data, particleSize, room ):
        print 'Saving average and baseline data to file'
        with open( room + particleSize + 'AvgBaseData.json', 'w') as fp:
            json.dump( data, fp )

    def loadAvgBaseData( self, particleSize, room ):
        with open( room + particleSize + 'AvgBaseData.json', 'r') as fp:
            return json.load(fp)

    def copyDatabase( self ):
        #Use following in command prompt. Not sure how to implement in Python
        #curl -X GET http://feresa.physics.unc.edu:5984/history_mjdscm/_all_docs?include_docs=true > database.txt
        pass
