import os
import random
import re as re
import pyhtml as ph
import now as now
import functions
from os.path import isfile, join
import xmltodict
import json
import ftfy
from datetime import datetime
import unidecode
import time
import logging

#2021-05-07
FOLDER_GEN_HTML = "generated_html"
FOLDER_ABC = "ABC_NAME_TO_DATE"
FOLDER_JSON = "c:\\Users\\abasc\\Documents\\_csaba\\my_fb_data_20200823\\messages\\inbox"   # dell
#FOLDER_JSON = "c:\\Users\\abasc\\Documents\\_code\\messenger_parser\\my_fb_data_20200823\\messages\\inbox\\"  # asus
FOLDER_BIG_FILES = "BIG_HTML_FILES"
FOLDER_HTML = "html"
FOLDER_PER_NAME_STATS = "perNameStats"
FOLDER_TXTS_FROM_JSON_OR_XML = "txtsFromJsonOrXml"
FOLDER_LOG = "log"
FILE_DONEFILE = "doneFile.txt"
XMLS_TO_TXT = "_txt_from_XML"
initFoldersList = [FOLDER_JSON, FOLDER_GEN_HTML, FOLDER_ABC, FOLDER_LOG, FOLDER_PER_NAME_STATS, FOLDER_TXTS_FROM_JSON_OR_XML]
STRING_VIDA_CSABA = 'Vida Csaba'

# END OF CONSTANTS

    #(filename="log"  + "/" + loggingFileName, encoding='utf-8', level=logging.DEBUG)

# STARTING PROGRAM HERE
startingTime = time.time()





def main():
    # Defining the start of the program
    now = datetime.now()
    dateNow = str(now.strftime("%Y%m%d_%Hh%Mm%Ss"))
    loggingFileName = "logfile_" + dateNow + ".log"
    logging.basicConfig(level=logging.DEBUG, filename="log" + "/" + loggingFileName)
    logging.info("Starting at : " + str(dateNow))
    functions.initFolders(initFoldersList)  # generated_html, log, json, abc

    # list of folders to process
    logging.info("That is " + str(len([name for name in os.listdir(FOLDER_TXTS_FROM_JSON_OR_XML) if os.path.isfile(name)])) + " files in folder " + FOLDER_TXTS_FROM_JSON_OR_XML)
    dirsToProcessInJsonFolder = os.listdir(FOLDER_JSON)
    #functions.processJsonToTxt(dirsToProcessInJsonFolder)
    functions.processTxtToDayFiles(FOLDER_TXTS_FROM_JSON_OR_XML)
    exit()
    functions.createTxtFilesFromFolders(dirsToProcessInJsonFolder)

#main()


counter = 0
fileCounter = 0
quotaToNameDict = {}
nameToQuotaDict = {}
messageCountToNameDict = {}
nameToCountDict = {}
diagramDataDict = {}
processedMenuPoints = {}
ABOUT_YOU = "about_you"
VISITED_JSON = "visited.json"
all_data = "my_fb_data_20200823"



# ===========================
# AFTER PROCESSING ALL FOLDER, PRINT TOP LISTS
# with open(FOLDER_GEN_HTML + '\\n' + "doneFile.txt", "w", encoding="utf-8") as doneF:
#     for line in doneFiles:
#         doneF.write('%s\n' % line)
# doneF.close()
#displayQuoteToNameDict(quotaToNameDict)
#displayMostMessagesDict(messageCountToNameDict)
#deleteEmptyFolders(FOLDER_GEN_HTML)



dayToCount = functions.showFilesInFolders(FOLDER_GEN_HTML)
print(dayToCount)

def getDailyCount(list, year, month, day):
    date = year  + "-" + month + "-" + day
    if date in list:
        count = list[date]
    else:
        count = 0
    return count

print(getDailyCount(dayToCount, "2013", "03", "03"))



dayToCount = functions.showFilesInFolders(FOLDER_GEN_HTML)
print(dayToCount)


functions.analyzeByYearAll(dayToCount)
yearMonthToCount = functions.analyzeByMonthsAll(dayToCount)
print(yearMonthToCount)
print("szar")
labels = yearMonthToCount


# all years to all the messages , eg: 2017: 6500 messages, 2018: 9800 messages;
# each year to all the months messages , eg: 2017: 01:5000, 02:3423,..., 12:2112 messages
# each month to stacked bars with percentage of how many with each person you talked with
# persons graph

# list of all the persons

# i need all the persons, and a list of the days, how many messages they talked


#analyzeByMonthsAll(dayToCount)









listOfAllPersonsInDayFiles = functions.getListOfAllPersonsInDayFiles(FOLDER_GEN_HTML)
print(listOfAllPersonsInDayFiles)
print(len(listOfAllPersonsInDayFiles))

#functions.processTxtFilesToDailyFiles(samplePath)
#listOfAllThePersons = getListOfAllPersonsInDayFiles(FOLDER_GEN_HTML)
#buildPersonFiles(listOfAllPersonsInDayFiles)

# expects always a list, even if it has only one element
def getDatasets(datasetList):

    ds1 = { "label" : '"Elso dataset label"', "backgroundColor" : "'rgb(255, 99, 132)'", "data" : "[0, 10, 5, 2, 20, 10, 45]"}
    ds2 = {"label": '"Masodik dataset label"', "backgroundColor": "'rgb(55, 99, 132)'", "data": "[10, 16, 25, 24, 20, 10, 5]"}
    dsList = [ds1, ds2]
    if datasetList:
        dsList = datasetList

    datasetsResult = ""

    for dataset in dsList:
        datasetJs = """
{
    label: %s,
    backgroundColor: %s,
    borderColor: 'rgb(255, 99, 132)',
    data: %s,
}
        
        """ % (dataset["label"], dataset["backgroundColor"], dataset["data"] )
        if datasetsResult:
            datasetsResult = datasetsResult + "," + datasetJs
        else:
            datasetsResult = datasetJs
    return datasetsResult


def getDiv(charts):
    myDiv = ""
    for chart in charts:
        print(chart)
        name = chart["name"]
        labelTag = name + "_label"
        data = name + "_data"
        id = name + "_id"
        labels = chart["labels"]
        datasetList = chart["datasets"]
        myDiv = myDiv + """
<div class="row">
    <canvas id="%s"></canvas>
  </div>

  <script>

const %s = 
  %s
;
const data = {
  labels: %s,
  datasets: [
  %s
  ]
};

const config = {
  type: 'line',
  data,
  options: {}
};

  // === include 'setup' then 'config' above ===


  var myChart = new Chart(
    document.getElementById('%s'),
    config
  );

</script>
    """ % (id, labelTag, labels, labelTag,  getDatasets(datasetList), id)
    return myDiv



def getHtmlFrame(charts):
    htmlFrame = """
    <!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>

<h1>Stats</h1>
<div class="container">

  %s

</div>
</body>
</html>
    
    
    
    """ % (getDiv(charts))
    return htmlFrame


def getKeysInList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list

def getValsInList(dict):
    list = []
    for key in dict.values():
        list.append(key)

    return list

datasetList = getValsInList(labels)
finalDataset = { "label" : '"Month to message count"', "backgroundColor" : "'rgb(25, 99, 132)'", "data" : str(datasetList)}
secondfinalDataset = { "label" : '"Month to message count"', "backgroundColor" : "'rgb(25, 99, 132)'", "data" : str(sorted(datasetList))}
print(str(datasetList))

chartYearmonthToCount_Labels = getKeysInList(labels)
chartYearmonthToCount_datasets = [finalDataset, secondfinalDataset]



charts = []  # all the charts must go into this list, they must be a json with a "labels" and a "datasets"

chartYearmonthToCount = {
    "name" : "chartYearmonthToCount",
    "labels" : chartYearmonthToCount_Labels,
    "datasets" : chartYearmonthToCount_datasets

}

chartYearmonthToCount_2 = {
    "name" : "justTryingSecondGraph",
    "labels" : chartYearmonthToCount_Labels,
    "datasets" : chartYearmonthToCount_datasets

}

charts.append(chartYearmonthToCount)
#charts.append(chartYearmonthToCount_2)



htmlFrame = getHtmlFrame(charts)
filename = functions.getDateOfNow() + "_" + functions.getTimeOfNow() + ".html"


def createHtml(filename, htmlFrame):
    fileNameWithPath = FOLDER_HTML + "\\" + filename
    with open(fileNameWithPath, "w", encoding="utf-8") as newFile:
        newFile.write(htmlFrame)
    newFile.close()
    print(fileNameWithPath + " generated.")


createHtml(filename, htmlFrame)

limitedPeople = functions.getListOfAllPersonsInDayFilesWithLimit(2000)
print(limitedPeople)
print(len(limitedPeople))

topMessages = functions.getTopMessagesWithinDAy()
print(topMessages)

# idea : get the top ten or twenty persons max count within a day, and order by date on a graph

exit()





#print(listOfAllThePersons)
#print(len(listOfAllThePersons))

# dt_string = now.strftime("%Y%m%d_%Hh%Mm%Ss")

endTime = time.time()
spentTime = endTime - startingTime
logging.info("Program runned for " + str(spentTime) + " seconds.")
#todo logging system


