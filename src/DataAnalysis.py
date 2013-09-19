from datetime import datetime, time, timedelta
from matplotlib import pyplot
from matplotlib.dates import date2num

class DataAnalysis():

    def __init__(self):
        pass

    def organizeDataArray( self, dataArray, startDate=datetime(2012,9,18), endDate=datetime.utcnow() ):
        dataDictionary = { 'Day Shift': {'Time': [], 'Count': []}, 'Night Shift': {'Time': [], 'Count': []}, 'Empty Lab': {'Time': [], 'Count': []} }
        dayStartTime = time(8,0,0)
        dayEndTime = time(17,0,0)
        nightStartTime = time(18,0,0)
        nightEndTime = time(0,0,0)
        emptyStartTime = time(0,0,0)
        emptyEndTime = time(7,0,0)
        for item in dataArray:
            itemTime = datetime.fromtimestamp( item['time'] ) - timedelta(hours=2)
            if itemTime >= startDate and itemTime <= endDate:
                if itemTime.time() >= dayStartTime and itemTime.time() < dayEndTime:
                    dataDictionary['Day Shift']['Time'].append( itemTime )
                    dataDictionary['Day Shift']['Count'].append( item['count'] )
                elif itemTime.time() >= nightStartTime or itemTime.time() < nightEndTime:
                    dataDictionary['Night Shift']['Time'].append( itemTime )
                    dataDictionary['Night Shift']['Count'].append( item['count'] )
                elif itemTime.time() >= emptyStartTime and itemTime.time() < emptyEndTime:
                    dataDictionary['Empty Lab']['Time'].append( itemTime )
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

        pyplot.figure(num=None, figsize=(16,9), dpi=100, facecolor='w', edgecolor='k')
        pyplot.plot_date(date2num(dayShiftDates),dayShiftCounts, 'r-')
        pyplot.plot_date(date2num(nightShiftDates),nightShiftCounts, 'g-')
        pyplot.plot_date(date2num(emptyLabDates),emptyLabCounts, 'b-')
        pyplot.xlabel( 'Date/Time (MT)' )
        pyplot.ylabel( 'Count' )
        pyplot.title( particleSize + ' um Counts' )
        pyplot.savefig( 'Plot' + particleSize + '.png' )

    def plotAllData( self, allData, particleSize ):
        dates = allData['Time']

        for shift in ['Day Shift','Night Shift','Empty Lab']:
            pyplot.figure(num=None, figsize=(16,9), dpi=100, facecolor='w', edgecolor='k')
            pyplot.plot_date(date2num(dates),allData[shift + ' Avg'], 'b-')
            pyplot.xlabel( 'Date (MT) ')
            pyplot.ylabel( 'Average Count' )
            pyplot.title( shift + ' Averages for ' + particleSize + 'um Counts' )
            pyplot.savefig( 'Avg' + shift[:-6] + particleSize + '.png')
            
        for shift in ['Day Shift','Night Shift','Empty Lab']:
            pyplot.figure(num=None, figsize=(16,9), dpi=100, facecolor='w', edgecolor='k')
            pyplot.plot_date(date2num(dates),allData[shift + ' Base'], 'b-')
            pyplot.xlabel( 'Date (MT)' )
            pyplot.ylabel( 'Baseline' )
            pyplot.title( shift + '  Baselines for ' + particleSize + ' um Counts' )
            pyplot.savefig( 'Base' + shift[:-6] + particleSize + '.png')

    def dateRange(self,startDate,endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def getAnalysisByDate( self, dataArray, startDate=datetime(2012,9,18), endDate=datetime.utcnow() ):
        data = {'Day Shift Avg': [], 'Night Shift Avg': [], 'Empty Lab Avg': [], 'Day Shift Base': [], 'Night Shift Base': [], 'Empty Lab Base': [], 'Time': []}
        for dateTime in self.dateRange(startDate,endDate):
            print ''
            print dateTime.strftime('%b %d, %Y')
            try:
                dataDictionary = self.organizeDataArray( dataArray, dateTime, dateTime + timedelta(1) )

                data['Time'].append(dateTime)
                
                averages = self.averageAllTimes(dataDictionary)
                data['Day Shift Avg'].append(averages['Day Shift'])
                print 'Average Day Shift Count: ' + str(averages['Day Shift'])
                data['Night Shift Avg'].append(averages['Night Shift'])
                print 'Average Night Shift Count: ' + str(averages['Night Shift'])
                data['Empty Lab Avg'].append(averages['Empty Lab'])
                print 'Average Empty Lab Count: ' + str(averages['Empty Lab'])

                baselines = self.getAllBaselines(dataDictionary)
                data['Day Shift Base'].append(baselines['Day Shift'])
                print 'Day Shift Baseline: ' + str(baselines['Day Shift'])
                data['Night Shift Base'].append(baselines['Night Shift'])
                print 'Night Shift Baseline: ' + str(baselines['Night Shift'])
                data['Empty Lab Base'].append(baselines['Empty Lab'])
                print 'Empty Lab Basline: ' + str(baselines['Empty Lab'])
            except ValueError:
                print "Error with Date's Data"
        return data
            

    def getBaseline( self, dataDictionary, shift ):
        counts = dataDictionary[shift]['Count'][:]
        for i in xrange(counts.count(0)):
            counts.remove(0)
        if len(counts) == 0:
            return 0
        minimum = min(counts)
        i = 0
        while i < len(counts):
            if abs(counts[i] - minimum) > 50:
                counts.remove(counts[i])
            else:
                i += 1
        return sum(counts)/float(len(counts))

    def getAllBaselines( self, dataDictionary ):
        return { 'Day Shift': self.getBaseline(dataDictionary,'Day Shift'),
                 'Night Shift': self.getBaseline(dataDictionary,'Night Shift'),
                 'Empty Lab': self.getBaseline(dataDictionary,'Empty Lab') }

    def getAverageCount( self, dataDictionary, shift ):
        counts = dataDictionary[shift]['Count'][:]
        for i in xrange(counts.count(0)):
            counts.remove(0)
        if len(counts) == 0:
            return 0
        return sum(counts)/float(len(counts))
    
        
    def averageAllTimes( self, dataDictionary ):
        return { 'Day Shift': self.getAverageCount(dataDictionary,'Day Shift'),
                 'Night Shift': self.getAverageCount(dataDictionary,'Night Shift'),
                 'Empty Lab': self.getAverageCount(dataDictionary,'Empty Lab') }
    
