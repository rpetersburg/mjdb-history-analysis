import DBController
import DataAnalysis
import sys
from datetime import datetime

class MJParticleDataAnalysis:
    def __init__(self):
        self.dbController = DBController.DBController()
        self.dataAnalysis = DataAnalysis.DataAnalysis()

    def run(self, particleSize='2.0', room='DR', startDate='09-18-2012', endDate=datetime.utcnow().strftime('%m-%d-%Y') ):
        dataArray = self.dbController.getParticleData( particleSize, room )
        try:
            print 'Attempting to Load Average and Baseline Data'
            allData = self.dbController.loadAvgBaseData( particleSize, room )
            print 'Load successful\n'
        except IOError:
            print 'Average and Baseline Data does not exist. Gathering and Saving Records'
            startDate = datetime.strptime(startDate,'%m-%d-%Y')
            endDate = datetime.strptime(endDate,'%m-%d-%Y')
            allData = self.dataAnalysis.getAnalysisByDate(dataArray,startDate,endDate)
            self.dbController.saveAvgBaseData( allData, particleSize, room )

        self.dataAnalysis.plotAllData( allData, particleSize, room )
        
        dataDictionary = self.dataAnalysis.organizeDataArray( dataArray, startDate, endDate )
        self.dataAnalysis.graphDataDictionary( dataDictionary, particleSize, room )

    def runAll(self):
        for room in ['DR','MS']:
            for particleSize in ['0.3','0.5','0.7','1.0','2.0','5.0']:
                self.run(particleSize, room)

    def saveParticleData( self ):
        for room in ['DR','MS']:
            for particleSize in ['0.3','0.5','0.7','1.0','2.0','5.0']:
                self.dbController.saveParticleDataFromDatabase(particleSize, room)
            

if __name__ == '__main__':
    app = MJParticleDataAnalysis()
    if len( sys.argv ) == 1:
        app.runAll()
    elif len( sys.argv ) == 2 and sys.argv[1] == 'save':
        app.saveParticleData()
    elif len( sys.argv ) == 2:
        app.run( str(sys.argv[1]) )
    elif len( sys.argv ) == 3:
        app.run( str(sys.argv[1]), str(sys.argv[2]) )
    elif len( sys.argv ) == 5:
        app.run( str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]) )
    else:
        print 'Invalid Arguments'
