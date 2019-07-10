import numpy
import csv
import datetime
import sys

def loadLokiData(filename, idfFile, conversionFile=None, conversionIDF=None, addArtificialRun=False, runLengthSecs=0):
    print "Loading "+filename+"..."
    
    with open(filename) as csvfile:
        lokidata_csv = list(csv.reader(csvfile, delimiter=" ", lineterminator='\r', skipinitialspace=True))
        for i in xrange(5):
            del lokidata_csv[:1]
        lokidata = numpy.array(lokidata_csv)
    
    convertIDF = False
    if conversionFile:
        print "Loading conversion file "+conversionFile+"..."
        convertIDF = True
        with open(conversionFile) as convCsvFile:
            convData = list(csv.reader(convCsvFile, delimiter=","))
            convData = numpy.array(convData)
            
            consStart = convData[:,0].astype(long)
            consEnd = convData[:,1].astype(long)
            start = convData[:,2].astype(long)
            end = convData[:,3].astype(long)
            
            convMap = {}
            for cs, ce, s, e in zip(consStart, consEnd, start, end): 
                # add 1 to end of range as xrange is not inclusive of last value
                convMap.update(zip(xrange(s, e+1), xrange(cs, ce+1)))
    
    tof = lokidata[:,9].astype(float) # milliseconds
    tof = tof*1000000.0 # convert to nanoseconds
    detids = [long(x, 16) for x in lokidata[:,-1]]
    detids = numpy.array(detids).astype(long)
    
    print detids

    print "Loading empty workspace..."
    try:
        ws = mtd["ws"]
    except:
        ws = LoadEmptyInstrument(idfFile, MakeEventWorkspace=True)
        
    if convertIDF:
        try:
            ws2 = mtd["ws2"]
        except:
            ws2 = LoadEmptyInstrument(conversionIDF, MakeEventWorkspace=True)

    numHists = ws.getNumberHistograms()

    detidToWsIndexMap = {}
    detidToWsIndexMapCons = {}
    
    pulsetime = datetime.datetime.now()

    print "Generating detector to workspace index maps..."
    for i in xrange(numHists):
        eventList = ws.getSpectrum(i)
        id = eventList.getDetectorIDs()
        detidToWsIndexMap[id[0]] = i
        eventList.clear(False)
        
        if convertIDF:
            eventList = ws2.getSpectrum(i)
            id = eventList.getDetectorIDs()
            detidToWsIndexMapCons[id[0]] = i
            eventList.clear(False)       

    added = 0
    iterations = 1
    pulsesPerSecond = 14
    
    if addArtificialRun:
        iterations = runLengthSecs * pulsesPerSecond
    
    print "Adding events to workspaces..."
    for run in xrange(iterations):
        for i in xrange(tof.size):
            if run == 0:
                listIndex = detidToWsIndexMap[detids[i]]
                eventList = ws.getSpectrum(listIndex)
                eventList.addEventQuickly(tof[i], DateAndTime(pulsetime.isoformat(sep="T")))
                added += 1
            
            if convertIDF:
                id = convMap[detids[i]]
                listIndex = detidToWsIndexMapCons[id]
                eventList = ws2.getSpectrum(listIndex)
                if i == 0:
                    print pulsetime.isoformat()
                eventList.addEventQuickly(tof[i],  DateAndTime(pulsetime.isoformat(sep="T"))) 
        pulsetime += datetime.timedelta(0, 1.0/pulsesPerSecond)
    tofmin = long(ws2.getTofMin())
    tofmax = long(ws2.getTofMax())
    width = tofmax - tofmin
    ptMin =  ws2.getPulseTimeMin()
    ptMax = ws2.getPulseTimeMax()
    
    print "Setting run info..."
    run = ws2.run()
    run.setStartAndEndTime(ptMin, ptMax)
    run.addProperty("run_number", "1", True)
    run.addProperty("run_start", str(ptMin), True)
    run.addProperty("TimeUnit", "Nano Seconds", True)
    print "Sorting events..."
    SortEvents(InputWorkspace='ws2', SortBy='Pulse Time')
    print "Rebinning workspace..."
    Rebin(InputWorkspace='ws2', OutputWorkspace='ws2_rebinned', Params=str(tofmin)+","+str(width)+","+str(tofmax))
    print str(added)+" events added!"
	
	SaveNexus(ws2, Filename="LokiEventData.nxs")
    
folder = ""
loadLokiData(folder+"lokiGeant4Data.out", folder+"LOKI_definition_test.xml", folder+"/LOKI_ID_Conversion.csv", folder+"LOKI_definition.xml", True, 1)