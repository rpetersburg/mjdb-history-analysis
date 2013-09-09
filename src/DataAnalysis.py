from datetime import datetime, time
from matplotlib import pyplot
from matplotlib.dates import date2num

class DataAnalysis():

    def __init__(self):
        self.dataDictionary = { 'Day Shift': [], 'Night Shift': [], 'Empty Lab': [] }
        pass

    def organizeDataArray( self, dataArray, startDate=datetime(2000,1,1), endDate=datetime.utcnow() ): 
        dayStartTime = time(2,0,0)
        nightStartTime = time(10,0,0)
        emptyStartTime = time(18,0,0)
        for item in dataArray:
            item['time'] = datetime.fromtimestamp( item['time'] )
            if item['time'] >= startDate and item['time'] <= endDate:
                if item['time'].time() >= dayStartTime and item['time'].time() < nightStartTime:
                    self.dataDictionary['Day Shift'].append( item )
                elif item['time'].time() >= nightStartTime and item['time'].time() < emptyStartTime:
                    self.dataDictionary['Night Shift'].append( item )
                elif item['time'].time() >= emptyStartTime or item['time'].time() < dayStartTime:
                    self.dataDictionary['Empty Lab'].append( item )
        return self.dataDictionary

    def graphDataDictionary( self, dataDictionary ):
        dayShiftDates = []
        dayShiftCounts = []
        nightShiftDates = []
        nightShiftCounts = []
        emptyLabDates = []
        emptyLabCounts = []
        for item in dataDictionary['Day Shift']:
            dayShiftDates.append(item['time'])
            dayShiftCounts.append(item['count'])
        for item in dataDictionary['Night Shift']:
            nightShiftDates.append(item['time'])
            nightShiftCounts.append(item['count'])
        for item in dataDictionary['Empty Lab']:
            emptyLabDates.append(item['time'])
            emptyLabCounts.append(item['count'])
        pyplot.plot_date(date2num(dayShiftDates),dayShiftCounts, 'b-')
        pyplot.plot_date(date2num(nightShiftDates),nightShiftCounts, 'r-')
        pyplot.plot_date(date2num(emptyLabDates),emptyLabCounts, 'g-')
        pyplot.xlabel( 'Date' )
        pyplot.ylabel( 'Count' )
        pyplot.show()
        
    
    def averageDayShift( self, dataDictionary ):
        dayShiftCounts = []
        dataArray = dataDictionary['Day Shift']
        for item in dataArray:
            dayShiftCounts.append( item['count'] )
        if len(dayShiftCounts) == 0:
            return 0
        return sum(dayShiftCounts)/float(len(dayShiftCounts))                   


    def averageNightShift( self, dataDictionary ):
        nightShiftCounts = []
        dataArray = dataDictionary['Night Shift']
        for item in dataArray:
            nightShiftCounts.append( item['count'] )
        if len(nightShiftCounts) == 0:
            return 0
        return sum(nightShiftCounts)/float(len(nightShiftCounts))


    def averageEmptyLab( self, dataDictionary ):
        emptyLabCounts = []
        dataArray = dataDictionary['Empty Lab']
        for item in dataArray:
            emptyLabCounts.append( item['count'] )
        if len(emptyLabCounts) == 0:
            return 0
        return sum(emptyLabCounts)/float(len(emptyLabCounts))
    
        
    def averageAllTimes( self, dataDictionary ):
        return { 'Day Shift': self.averageDayShift(dataDictionary),
                 'Night Shift': self.averageNightShift(dataDictionary),
                 'Empty Lab': self.averageEmptyLab(dataDictionary) }
    
