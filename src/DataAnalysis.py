from datetime import datetime

class DataAnalysis():

    def __init__(self):
        self.dayShiftCounts = []
        self.nightShiftCounts = []
        self.emptyLabCounts = []

    
    def averageDayShift( self, dataArray, startDate, endDate ):
        startTime = datetime.time(2,0,0)
        endTime = datetime.time(10,0,0)
        for item in dataArray:
            dateTimeObj = datetime.fromtimestamp(item['time'])
            if dateTimeObj.date() >= startDate and dateTimeObj.date() =< endDate:
                if dateTimeObj.time() >= startTime and dateTimeObj.time() <= endTime:
                    self.dayShiftCounts.append( item['count'] )
        return sum(self.dayShiftCounts)/float(len(self.dayShiftCounts))                   


    def averageNightShift( self, dataArray, startDate, endDate ):
        startTime = datetime.time(10,0,0)
        endTime = datetime.time(18,0,0)
        pass


    def averageEmptyLab( self, dataArray, startDate, endDate ):
        startTime = datetime.time(18,0,0)
        endTime = datetime.time(2,0,0)
        pass

    
