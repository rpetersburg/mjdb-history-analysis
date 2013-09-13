import DBController
import DataAnalysis
import sys
from datetime import datetime

class MJParticleDataAnalysis:
    def __init__(self):
        self.dbController = DBController.DBController()
        self.dataAnalysis = DataAnalysis.DataAnalysis()

    def run(self, particleSize='0.5'):
        dataArray = self.dbController.getParticleData( particleSize )

        startDate = datetime(2013,6,1)
        endDate = datetime(2013,9,8)
        allData = self.dataAnalysis.getAnalysisByDate(dataArray,startDate,endDate)

        self.dataAnalysis.plotAllData( allData, particleSize )
        
        dataDictionary = self.dataAnalysis.organizeDataArray( dataArray, startDate, endDate )
        self.dataAnalysis.graphDataDictionary( dataDictionary, particleSize )

    def saveParticleData( self ):
        for particleSize in ['0.3','0.5','0.7','1.0','2.0','5.0']:
            self.dbController.saveParticleDataFromDatabase(particleSize)
            

if __name__ == '__main__':
    app = MJParticleDataAnalysis()
    if len( sys.argv ) == 1:
        app.run()
    elif len( sys.argv ) == 2 and sys.argv[1] == 'save':
        app.saveParticleData()
    elif len( sys.argv ) == 2 and sys.argv[1] != 'save':
        app.run( str(sys.argv[1]) )
    else:
        print 'Invalid Arguments'
