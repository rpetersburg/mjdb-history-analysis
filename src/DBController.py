import json
import getpass
import couchdb
from datetime import datetime

class DBController():

    def __init__(self):
        self.couchURL = 'https://http://feresa.physics.unc.edu:5984/_utils'
        self.couch = couchdb.Server( self.couchURL )
        print 'Please authenticate for ' + self.couchURL
        self.username = raw_input('Enter username: ')
        self.password = getpass.getpass('Enter password: ')
        self.couch.resource.credentials = ( self.username, self.password )
        self.db = self.couch['history_mjdscm']

    
    def getParticleData( self ):
        for rec in self.db:
            if 'adcs' not in self.db[rec]:
                continue
            elif 
