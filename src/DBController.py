import json
import couchdb
from datetime import datetime
from matplotlib import dates

class DBController():

    def __init__(self):
        self.couchURL = 'http://feresa.physics.unc.edu:5984/'
        self.couch = couchdb.Server( self.couchURL )
        self.db = self.couch['history_mjdscm']

    
    def appendParticleData( self, particleRec, particleSize, dataArray, timeArray ):
        if particleSize == ('0.3' or '0.5' or '0.7' or '1.0' or '2.0' or '5.0'):
            dataArray.append(self.db[particleRec]['adcs'][0]['MS ' + particleSize + ' um count'])
            timeArray.append(self.getDateTimeObject(self.db[rec]['timestamp']))
        else:
            print 'Invalid Particle Size'
            
    def getDateTimeObject( self, string ):
        return datetime.strptime(string, '%Y/%m/%d %H:%M:%S')

    def iterator():
        for rec in



dbController = DBController()
rec = '00f8e4c5c894ec099abc8a1e2f000a0b'
dataArray = []
timeArray = []
dbController.appendParticleData( rec, dataArray, timeArray )
print dataArray
dates = dates.date2num(timeArray)
print timeArray
print dates
