import json
import couchdb
from datetime import datetime
from matplotlib import dates

class DBController():

    def __init__(self):
        self.couchURL = 'http://feresa.physics.unc.edu:5984/'
        self.couch = couchdb.Server( self.couchURL )
        self.db = self.couch['history_mjdscm']
        self.dataArray = []
        self.timeArray = []

    
    def appendParticleData( self, particleRec, particleSize, dataArray, timeArray ):
        try:
            for item in self.db[ particleRec ]['adcs']:
                if ('DR ' + particleSize + ' um count') in item:
                    dataArray.append( item['DR ' + particleSize + ' um count'] )
                    timeArray.append( self.db[ particleRec ][ 'time' ] )
        except KeyError, TypeError:
            print 'Invalid Particle Size'

    def iterator( self, particleSize ):
        n = 0
        print 'Starting'
        for rec in self.db:
            print 'Iterating'
            if n > 10:
                break
            elif 'adcs' in rec:
                print "Hooray"
                appendParticleData( rec, particleSize, self.dataArray, self.timeArray )
            else:
                print 'Oh no!'
            n += 1
                



dbController = DBController()
dbController.iterator('0.5')
print dbController.dataArray
##dates = dates.date2num(timeArray)
print dbController.timeArray
##print dates
