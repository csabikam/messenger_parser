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


def createTxtFilesFromFolders(dirsToProcessInJsonFolder):
    for folderPath in dirsToProcessInJsonFolder:
        print(folderPath)
        filesOrFoldersInFolder = os.listdir(folderPath)
        print(filesOrFoldersInFolder)
        exit()
        jsonFiles = list(filter(lambda x: (str(x).endswith('.json')), filesOrFoldersInFolder))
        xmlFiles = list(filter(lambda x: (str(x).endswith('.xml')), filesOrFoldersInFolder))
        logging.info("List of json files " + str(jsonFiles))
        logging.info("List of xml files " + str(xmlFiles))
        print("List of json files " + str(jsonFiles))
        print("List of xml files " + str(xmlFiles))
        counter = 0
        if jsonFiles != []:
            logging.info("Json files : " + str(jsonFiles))
            for file in jsonFiles:
                file = folderPath + '/' + file
                # volt: counter = counter +
                functions.processJson(file)
        pass


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
    createTxtFilesFromFolders(dirsToProcessInJsonFolder)

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

def showFilesInFolders(pathToGenerated):
    count = 0
    dayToCountDict = {}
    for x in os.walk(pathToGenerated):
        #print(x[0])
        if not(x[1]):
            day = x[0]
            count += 1
            sumOfAllLines = 0
            for chat in x[2]:
                #print(chat)
                #print(sumOfAllLines)
                try:
                    numOfLines = int((chat.split("_")[1]).split(".")[0])
                    sumOfAllLines = numOfLines + sumOfAllLines
                except IndexError:
                    print("Oops!  That was no valid number.  Try again..." + chat)

                #print(numOfLines)


            #print("sum of all: " + str(sumOfAllLines))
            if len(day.split("\\")) == 4:
                month = day.split("\\")[2]
                thatDay = day.split("\\")[3]
                date = day.split("\\")[1] + "-" + month + "-" + thatDay
                dayToCountDict[date] = sumOfAllLines
            #print(day)
            #print(str(x))
            #print(len(x[2]))
            #print(count)
    #print(count)
    dictionary_items = dayToCountDict.items()
    sorted_items = sorted(dictionary_items)
    #print(sorted_items)
    #print(type(sorted_items))

    return dayToCountDict

dayToCount = showFilesInFolders(FOLDER_GEN_HTML)
print(dayToCount)

def getDailyCount(list, year, month, day):
    date = year  + "-" + month + "-" + day
    if date in list:
        count = list[date]
    else:
        count = 0
    return count

print(getDailyCount(dayToCount, "2013", "03", "03"))



dayToCount = showFilesInFolders(FOLDER_GEN_HTML)
print(dayToCount)




def analyzeByYearAll(dayToCount):
    #print(dayToCount)
    yearToCount = {}
    for date, val in dayToCount.items():
        #print(date + " " + str(val))
        year = date.split("-")[0]
        if year in yearToCount:
            yearToCount[year] = yearToCount[year] + val
        else:
            yearToCount[year] = val
    print(yearToCount)

analyzeByYearAll(dayToCount)


def analyzeByMonthsAll(dayToCount):
    #print(dayToCount)
    yearMonthToCount = {}
    for date, val in dayToCount.items():
        #print(date + " " + str(val))
        year = date.split("-")[0]
        month = date.split("-")[1]
        yearMonth = year + "-" + month
        if yearMonth in yearMonthToCount:
            yearMonthToCount[yearMonth] = yearMonthToCount[yearMonth] + val
        else:
            yearMonthToCount[yearMonth] = val
    print(yearMonthToCount)
    return yearMonthToCount

yearMonthToCount = analyzeByMonthsAll(dayToCount)
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


def getListOfAllPersonsInDayFiles(pathToGenerated):
    persons = []
    for x in os.walk(pathToGenerated):
        files = x[2]
        for file in files:
            name = file.split("_")[0]
            persons.append(name)
    return sorted(list(set(persons)))

def getListOfAllPersonsInDayFilesWithLimit(limit):
    persons = []
    for x in os.walk(FOLDER_GEN_HTML):
        files = x[2]
        for file in files:
            name = file.split("_")[0]
            count = int((file.split("_")[1]).split(".")[0])
            if count > limit:
                persons.append(name)
                print(x)
                print(file)
    return sorted(list(set(persons)))

# TOPLIST - MOST CHATTED WITHIN A DAY - who is the one you talked the most within a day
def getTopMessagesWithinDAy():
    max = 0
    person = ""
    day = ""
    for x in os.walk(FOLDER_GEN_HTML):
        files = x[2]
        for file in files:
            name = file.split("_")[0]
            count = int((file.split("_")[1]).split(".")[0])
            if count > max:
                max = count
                day = x[0]
                person = name
    print("The person you chatted the most within a day was " + person + " , and you changed " + str(max) + " messages on " + str(day))


listOfAllPersonsInDayFiles = getListOfAllPersonsInDayFiles(FOLDER_GEN_HTML)
print(listOfAllPersonsInDayFiles)
print(len(listOfAllPersonsInDayFiles))



def getProperDateFormat(filesPerDay):
    month = filesPerDay.split("\\")[2]
    day = filesPerDay.split("\\")[3]
    result = filesPerDay.split("\\")[1] + "-" + month + "-" + day
    return result


def buildOnePersonFile(person):
    dayToCountList = []
    print("person is " + person)
    sum = 0
    for filesPerDay in os.walk(FOLDER_GEN_HTML):
        files = filesPerDay[2]
        for file in files:
            name = file.split("_")[0]
            if (name == person):
                thatDate = getProperDateFormat(filesPerDay[0])
                count = (file.split("_")[1]).split(".")[0]
                sum = sum + int(count)
                recentDayToCountDict = {}
                recentDayToCountDict[thatDate] =  count
                dayToCountList.append(recentDayToCountDict)
    fileNameWithPath = FOLDER_PER_NAME_STATS + "\\" + person + "_" + str(sum) + ".stat"
    print(dayToCountList)
    with open(fileNameWithPath, "w", encoding="utf-8") as newFile:
        for record in dayToCountList:
            key = list(record.keys())[0]
            newFile.write(key + " : " + record[key])
            newFile.write("\n")
    newFile.close()



def buildPersonFiles(listOfAllThePersons):
    for person in listOfAllThePersons:
        print("Building PERSON(DATE:COUNT) file for person : " + person)
        buildOnePersonFile(person)


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
    datasets = """
{
    label: 'My First dataset',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 2, 20, 10, 45],
  },
  {
    label: 'My second dataset',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(55, 99, 132)',
    data: [45, 20, 5, 30, 20, 30, 40],
  }
    """
    return datasets


def getLabels(labels):
    if labels:
        return labels
    else:
        return """'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July'"""


def getDiv(labels, datasetList):
    myDiv = """
    
<div class="row">
    <canvas id="myChart"></canvas>
  </div>

  <script>


const labels = 
  %s
;
const data = {
  labels: labels,
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
    document.getElementById('myChart'),
    config
  );

</script>
    """ % (getLabels(labels), getDatasets(datasetList))
    return myDiv



def getHtmlFrame(labels, datasetList):
    sample = """line %d
          line %d
          line %d""" % (
        1,
        2,
        3)

    htmlFrame = """
    <!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>

<h1>Stats</h1>
<li> %s </li>
<div class="container">
    <h3> %s </h3>
  %s

</div>


</body>

</html>
    
    
    
    """ % ("TOP LIST OF COUNT OF MESSAGES x", "Other text to H3", getDiv(labels, datasetList))
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


labelsList = getKeysInList(labels)

htmlFrame = getHtmlFrame(labelsList, [finalDataset, secondfinalDataset])
filename = functions.getDateOfNow() + "_" + functions.getTimeOfNow() + ".html"


def createHtml(filename, htmlFrame):
    fileNameWithPath = FOLDER_HTML + "\\" + filename
    with open(fileNameWithPath, "w", encoding="utf-8") as newFile:
        newFile.write(htmlFrame)
    newFile.close()
    print(fileNameWithPath + " generated.")


createHtml(filename, htmlFrame)

limitedPeople = getListOfAllPersonsInDayFilesWithLimit(2000)
print(limitedPeople)
print(len(limitedPeople))

topMessages = getTopMessagesWithinDAy()
print(topMessages)

# idea : get the top ten or twenty persons max count within a day, and order by date on a graph

exit()





#print(listOfAllThePersons)
#print(len(listOfAllThePersons))


def generateSumHtml():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%Hh%Mm%Ss")
    #print(dt_string)
    pass

def getPhases():
    PHASES = []
    return PHASES



generateSumHtml()
endTime = time.time()
spentTime = endTime - startingTime
logging.info("Program runned for " + str(spentTime) + " seconds.")
#todo logging system


