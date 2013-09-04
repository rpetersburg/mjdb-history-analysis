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

    
    def getParticleData( self, particleRec, index, particleSize ):
        try:
            return {'count': self.db[particleRec]['adcs'][index]['DR ' + particleSize + ' um count'] , 'time': self.db[particleRec]['time'] }
        except KeyError, TypeError:
            print 'Invalid Particle Size'
            return {'count': None, 'time': None}


    def iterator( self, particleSize ):
        n = 0
        for rec in self.couchdb_pager(self.db):
            if n>10:
                break
            if 'adcs' in self.db[ rec ]:
                for item in self.db[ rec ]['adcs']:
                    if ('DR ' + particleSize + ' um count') in item:
                        self.dataArray.append( self.getParticleData( rec, self.db[rec]['adcs'].index(item), particleSize ) )
                        n+=1

            
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
                    



dbController = DBController()
dbController.iterator('0.5')
print dbController.dataArray
