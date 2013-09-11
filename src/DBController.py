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

    def getParticleDataFromAllData( self, particleSize, allData ):
        dataArray = []
        print 'Getting ' + particleSize + ' from all data'
        for rec in allData:
            dataArray.append( self.getParticleCount( rec, particleSize ) )
        self.saveParticleData(dataArray, particleSize)
        return dataArray
            
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
        with open('particleData' + str(particleSize) + '.json', 'w') as fp:
            json.dump(dataArray, fp)

    def loadParticleData( self, particleSize ):
        with open('particleData' + str(particleSize) + '.json', 'r') as fp:
            return json.load(fp)


    def getAllData( self ):
        try:
            print 'Attempting to Load All Data'
            allData = self.loadParticleData('')
            print 'Load Successful'
        except IOError:
            print 'Saved Data does not exist. Gathering and Saving Records'
            allData = self.getAllDataFromDatabase()
            self.saveAllData(allData)
        return allData

    def getAllDataFromDatabase( self ):
        print 'Getting Data from Database'
        with open('database.json', 'r') as database:
            allData = []
            n = 1
            print 'Organizing data'
            for rec in database:
                if n % 1000 == 0:
                    print n ,
                try:
                    recDict = json.loads(rec[0:-2])
                    if recDict['id'][0] == '_':
                        continue
                    if recDict['doc']['title'][6:9] == 'SCM':
                        allData.append( { 'adcs': recDict['doc']['adcs'], 'time': recDict['doc']['time'] } )
                except (KeyError,ValueError) as e:
                    print n, e
                    print rec
                n += 1
        self.saveAllData( allData )

    def saveAllData( self, allData ):
        with open('particleData.json', 'w') as fp:
            json.dump(allData, fp)

    def copyDatabase( self ):
        #Use following in command prompt. Not sure how to implement in Python
        #curl -X GET http://feresa.physics.unc.edu:5984/history_mjdscm/_all_docs?include_docs=true > database.txt
        pass

    # This is not my own function. I am using public domain code by Marcus Brinkmann that speeds up couchDB iteration time
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
