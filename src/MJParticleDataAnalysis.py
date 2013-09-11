import DBController
import DataAnalysis
import sys

class MJParticleDataAnalysis:
    def __init__(self):
        self.dbController = DBController.DBController()
        self.dataAnalysis = DataAnalysis.DataAnalysis()

    def run(self, particleSize='0.5'):
        allData = self.dbController.getAllData()
        dataArray = self.dbController.getParticleData( particleSize, allData )

        dataDictionary = self.dataAnalysis.organizeDataArray( dataArray )
        averages = self.dataAnalysis.averageAllTimes(dataDictionary)
        print 'Average Day Shift Count: ' + str(averages['Day Shift'])
        print 'Average Night Shift Count: ' + str(averages['Night Shift'])
        print 'Average Empty Lab Count: ' + str(averages['Empty Lab'])
        self.dataAnalysis.graphDataDictionary( dataDictionary )

    def saveParticleData( self ):
        allData = self.dbController.getAllDataFromDatabase()
            

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
