from datetime import datetime, time, timedelta
from matplotlib import pyplot
from matplotlib.dates import date2num

class DataAnalysis():

    def __init__(self):
        pass

    def organizeDataArray( self, dataArray, startDate=datetime(2000,1,1), endDate=datetime.utcnow() ):
        dataDictionary = { 'Day Shift': {'Time': [], 'Count': []}, 'Night Shift': {'Time': [], 'Count': []}, 'Empty Lab': {'Time': [], 'Count': []} }
        dayStartTime = time(7,30,0)
        nightStartTime = time(16,30,0)
        emptyStartTime = time(0,0,0)
        for item in dataArray:
            item['time'] = datetime.fromtimestamp( item['time'] ) - timedelta(hours=2)
            if item['time'] >= startDate and item['time'] <= endDate:
                if item['time'].time() >= dayStartTime and item['time'].time() < nightStartTime:
                    dataDictionary['Day Shift']['Time'].append( item['time'] )
                    dataDictionary['Day Shift']['Count'].append( item['count'] )
                elif item['time'].time() >= nightStartTime or item['time'].time() < emptyStartTime:
                    dataDictionary['Night Shift']['Time'].append( item['time'] )
                    dataDictionary['Night Shift']['Count'].append( item['count'] )
                elif item['time'].time() >= emptyStartTime and item['time'].time() < dayStartTime:
                    dataDictionary['Empty Lab']['Time'].append( item['time'] )
                    dataDictionary['Empty Lab']['Count'].append( item['count'] )
        for shift in ['Day Shift','Night Shift','Empty Lab']:
            dataDictionary[shift]['Time'], dataDictionary[shift]['Count'] = (list(t) for t in zip(*sorted(zip(dataDictionary[shift]['Time'], dataDictionary[shift]['Count']))))
        return dataDictionary

    def graphDataDictionary( self, dataDictionary, particleSize ):
        dayShiftDates = dataDictionary['Day Shift']['Time']
        dayShiftCounts = dataDictionary['Day Shift']['Count']
        nightShiftDates = dataDictionary['Night Shift']['Time']
        nightShiftCounts = dataDictionary['Night Shift']['Count']
        emptyLabDates = dataDictionary['Empty Lab']['Time']
        emptyLabCounts = dataDictionary['Empty Lab']['Count']
        
        pyplot.plot_date(date2num(dayShiftDates),dayShiftCounts, 'r-')
        pyplot.plot_date(date2num(nightShiftDates),nightShiftCounts, 'g-')
        pyplot.plot_date(date2num(emptyLabDates),emptyLabCounts, 'b-')
        pyplot.xlabel( 'Date (MT)' )
        pyplot.ylabel( 'Count' )
        pyplot.title( particleSize + ' um Counts' )
        pyplot.show()

    def getBaselines( self, dataDictionary ):
        dayShiftCounts = data

    def getAverageCount( self, dataDictionary, shift ):
        counts = dataDictionary[shift]['Count']
        if len(counts) == 0:
            return 0
        return sum(counts)/float(len(counts))
    
        
    def averageAllTimes( self, dataDictionary ):
        return { 'Day Shift': self.getAverageCount(dataDictionary,'Day Shift'),
                 'Night Shift': self.getAverageCount(dataDictionary,'Night Shift'),
                 'Empty Lab': self.getAverageCount(dataDictionary,'Empty Lab') }
    
