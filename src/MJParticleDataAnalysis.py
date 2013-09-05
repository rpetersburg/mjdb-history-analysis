import DBController
import DataAnalysis
import sys

class MJParticleDataAnalysis:
    def __init__(self):
        self.dbController = DBController.DBController()
        self.dataAnalysis = DataAnalysis.DataAnalysis()

    def run(self, particleSize='0.3'):
        try:
            print 'Attempting to Load Saved Data'
            dataArray = self.dbController.loadParticleData(particleSize)
            print 'Load Successful'
        except IOError:
            print 'Saved Data Does not Exist. Gathering and Saving Records'
            dataArray = self.dbController.getParticleData( particleSize )
            self.dbController.saveParticleData( dataArray, particleSize )
        dataDictionary = self.dataAnalysis.organizeDataArray( dataArray )
        averages = self.dataAnalysis.averageAllTimes(dataDictionary)
        print 'Average Day Shift Count: ' + str(averages['Day Shift'])
        print 'Average Night Shift Count: ' + str(averages['Night Shift'])
        print 'Average Empty Lab Count: ' + str(averages['Empty Lab'])
##        self.dataAnalysis.graphDataDictionary( dataDictionary )

if __name__ == '__main__':
    if len( sys.argv ) == 1:
        app = MJParticleDataAnalysis()
        app.run()
    if len( sys.argv ) == 2:
        app = MJParticleDataAnalysis()
        app.run( str(sys.argv[1]) )
