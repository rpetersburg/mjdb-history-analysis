import DBController
import DataAnalysis
import sys
from datetime import datetime

class MJParticleDataAnalysis:
    def __init__(self):
        self.dbController = DBController.DBController()
        self.dataAnalysis = DataAnalysis.DataAnalysis()

    def run(self, particleSize='2.0', startDate='09-18-2012', endDate=datetime.utcnow().strftime('%m-%d-%Y') ):
        dataArray = self.dbController.getParticleData( particleSize )
        try:
            print 'Attempting to Load Average and Baseline Data'
            allData = self.dbController.loadAvgBaseData( particleSize )
            print 'Load successful\n'
        except IOError:
            print 'Average and Baseline Data does not exist. Gathering and Saving Records'
            startDate = datetime.strptime(startDate,'%m-%d-%Y')
            endDate = datetime.strptime(endDate,'%m-%d-%Y')
            allData = self.dataAnalysis.getAnalysisByDate(dataArray,startDate,endDate)
            self.dbController.saveAvgBaseData( allData, particleSize )

        self.dataAnalysis.plotAllData( allData, particleSize )
        
        dataDictionary = self.dataAnalysis.organizeDataArray( dataArray, startDate, endDate )
        self.dataAnalysis.graphDataDictionary( dataDictionary, particleSize )

    def runAll(self):
        for particleSize in ['0.3','0.5','0.7','1.0','2.0','5.0']:
            self.run(particleSize)

    def saveParticleData( self ):
        for particleSize in ['0.3','0.5','0.7','1.0','2.0','5.0']:
            self.dbController.saveParticleDataFromDatabase(particleSize)
            

if __name__ == '__main__':
    app = MJParticleDataAnalysis()
    if len( sys.argv ) == 1:
        app.runAll()
    elif len( sys.argv ) == 2 and sys.argv[1] == 'save':
        app.saveParticleData()
    elif len( sys.argv ) == 2 and sys.argv[1] != 'save':
        app.run( str(sys.argv[1]) )
    elif len( sys.argv ) == 3:
        app.run( str(sys.argv[1]), str(sys.argv[2]) )
    elif len( sys.argv ) == 4:
        app.run( str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]) )
    else:
        print 'Invalid Arguments'
