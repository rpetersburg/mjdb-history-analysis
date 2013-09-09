import json
import couchdb
from datetime import datetime
from matplotlib import dates

class DBController():

    def __init__(self):
        self.couchURL = 'http://feresa.physics.unc.edu:5984/'
        self.couch = couchdb.Server( self.couchURL )
        self.db = self.couch['history_mjdscm']


    def getParticleData( self, particleSize , allData ):
        try:
            print 'Attempting to Load Particle Data'
            dataArray = self.loadParticleData( particleSize )
            print 'Load Successful'
        except IOError:
            print 'Particle Data does not exist. Gathering and Saving Records'
            dataArray = self.getParticleDataFromAllData( particleSize, allData )
            self.saveParticleData( dataArray, particleSize )
        return dataArray


    def getParticleDataFromAllData( self, particleSize, allData, startDate=datetime(2013,5,1), endDate = datetime.utcnow() ):
        dataArray = []
        n = 1
        for rec in allData:
            if rec['title'] == 'Davis SCM Environmental Monitoring Processes':
                recTime = datetime.fromtimestamp(rec['time'])
                if recTime > startDate and recTime < endDate:
                    dataArray.append( self.getParticleCount( rec, particleSize ) )
                    print n ,
                    n += 1
        return dataArray

    def getAllData( self ):
        try:
            print 'Attempting to Load All Data'
            allData = self.loadParticleData('')
            print 'Load Successful'
        except IOError:
            print 'Saved Data does not exist. Gathering and Saving Records'
            allData = self.getAllDataFromDatabase()
        return allData

    def getAllDataFromDatabase( self, startPoint, endPoint ):
        allData = self.loadParticleData( '' )
        n = 1
        for rec in self.couchdb_pager(self.db):
            if n > endPoint:
                break
            if n > startPoint:
                if self.db[rec]['title'][6:9] == 'SCM':
                    allData.append( self.db[rec] )
                    self.saveAllData( allData )
                    print n ,
            n += 1
        return allData

    def saveAllData( self, allData ):
        with open('particleData.json', 'wb') as fp:
            json.dump(allData, fp)
        
    
    def getParticleCount( self, particleRec, particleSize ):
        if str(particleSize) == '0.3':
            index = 8
        elif str(particleSize) == '0.5':
            index = 9
        elif str(particleSize) == '0.7':
            index = 10
        elif str(particleSize) == '1.0':
            index = 11
        elif str(particleSize) == '2.0':
            index = 12
        elif str(particleSize) == '5.0':
            index = 13
        else:
            print 'Invalid Particle Size'
            return {'count': None, 'time': None}
        return {'count': particleRec['adcs'][index]['DR ' + str(particleSize) + ' um count'] , 'time': particleRec['time'] }


    def saveParticleData( self, dataArray, particleSize ):
        with open('particleData' + str(particleSize) + '.json', 'wb') as fp:
            json.dump(dataArray, fp)

    def loadParticleData( self, particleSize ):
        with open('particleData' + str(particleSize) + '.json', 'rb') as fp:
            return json.load(fp)


    # This is not my own function. I am using a public domain function by Marcus Brinkmann that speeds up couchDB iteration time #
    def couchdb_pager(self, db, view_name='_all_docs', startkey=None, startkey_docid=None, endkey=None, endkey_docid=None, bulk=5000):
        # Request one extra row to resume the listing there later.
        options = {'limit': bulk + 1}
        if startkey:
            options['startkey'] = startkey
            if startkey_docid:
                options['startkey_docid'] = startkey_docid
        if endkey:
            options['endkey'] = endkey
            if endkey_docid:
                options['endkey_docid'] = endkey_docid
        done = False
        while not done:
            view = self.db.view(view_name, **options)
            rows = []
            # If we got a short result (< limit + 1), we know we are done.
            if len(view) <= bulk:
                done = True
                rows = view.rows
            else:
                # Otherwise, continue at the new start position.
                rows = view.rows[:-1]
                last = view.rows[-1]
                options['startkey'] = last.key
                options['startkey_docid'] = last.id

            for row in rows:
                yield row.id
