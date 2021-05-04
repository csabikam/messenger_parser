import os
import random
import re

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

#2021-01-29
FOLDER_GEN_HTML = "generated_html"
FOLDER_ABC = "ABC_NAME_TO_DATE"
FOLDER_JSON = "c:\\Users\\abasc\\Documents\\_csaba\\my_fb_data_20200823\\messages\\inbox"
FOLDER_BIG_FILES = "BIG_HTML_FILES"
FOLDER_LOG = "log"
FILE_DONEFILE = "doneFile.txt"
XMLS_TO_TXT = "_txt_from_XML"
initFoldersList = [FOLDER_JSON, FOLDER_GEN_HTML, FOLDER_ABC, FOLDER_LOG]
STRING_VIDA_CSABA = 'Vida Csaba'
# END OF CONSTANTS
now = datetime.now()
dateNow = str(now.strftime("%Y%m%d_%Hh%Mm%Ss"))
loggingFileName = "logfile_" + dateNow + ".log"
logging.basicConfig(level=logging.DEBUG, filename="log" + "/" + loggingFileName)
    #(filename="log"  + "/" + loggingFileName, encoding='utf-8', level=logging.DEBUG)

# STARTING PROGRAM HERE
startingTime = time.time()
logging.info("Starting at : " + str(dateNow))
functions.initFolders(initFoldersList) # generated_html, log, json, abc
filesAlreadyDone = functions.getDoneFiles()
logging.info("Files already done: ")
logging.info(filesAlreadyDone)
now = datetime.now()
#f= open(loggingFileName,"x")
#f.close()
dirsToProcessInJsonFolder = os.listdir(FOLDER_JSON)
logging.info("Folders to process")
logging.info(dirsToProcessInJsonFolder)
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

def f_links(ctx):
    for title, page in [('Home', '/home.html'),
                        ('Login', '/login.html')]:
        yield ph.li(ph.a(href=page)(title))

def processVisited(pathToFile):
    print(pathToFile + " szar")
    menuElements = []
    with open(pathToFile) as json_file:
        data = json.load(json_file)
        for key in data["visited_things"]:
            name = functions.encodeText(str(key['name']))
            print(name)
            print(str(key))
            menuElements.append((name, name))

    def f_links(ctx):
        for title, page in menuElements:
            yield ph.li(ph.a(href=page)(title))
    t = ph.html(
        ph.head(
            ph.title('visited_things'),
            ph.script(src="http://path.to/script.js")
        ),
        ph.body(
            ph.header(
                ph.img(src='/path/to/logo.png'),
                ph.nav(
                    ph.ul(f_links(menuElements))
                )
            ),
            ph.div(
                lambda ctx: "Hello %s" % ctx.get('user', 'Guest'),
                'Content here'
            ),
            ph.footer(
                ph.hr,
                'Copyright 2013'
            )
        )
    )
    resultFile = FOLDER_GEN_HTML + "\\" + "sample.html"
    with open(resultFile, "w", encoding="utf-8") as newFile:
        newFile.write(t.render(user='Csaba'))
    newFile.close()

    print(str(menuElements))

    exit()

def processAboutYou(path):
    print(path + " ===== ")
    content = os.walk(path)
    for files in content:
        for file in files[2]:
            if file == VISITED_JSON :
                pathToFile = path + "\\" + VISITED_JSON
                processVisited(pathToFile)
                print(file)

def processAllData(all_data):
    counter = 0
    dirs = os.walk(all_data)
    for folder in dirs:
        counter += 1
        if counter > 60:
            exit()
        else:
            print(counter)
            print(folder)

            if (folder[1] == []) & (folder[2] == []):
                print("Should be deleted: " + str(folder))
            if folder[0] == all_data + "\\"  + ABOUT_YOU:
                print("Start aboutyou")
                processAboutYou(folder[0])
                exit()



    exit()

#processAllData(all_data)

def processJsonToTxtAndThenToDayFiles():
    # the main program to prepare corrected txt files from json, and creating day files in structured order
    # ===========================
    for folder in dirsToProcessInJsonFolder:
        logging.info("Start processing folder \"" + folder + "\"")
        print("Start processing folder \"" + folder + "\"")
        # exit()
        print("Start processing folder \"" + folder + "\"")
        folderPath = FOLDER_JSON + '/' + folder
        logging.info("Relative path to folder " + folderPath)
        filesInFolder = os.listdir(folderPath)
        logging.info("Files in: " + folderPath)
        print("Files in: " + folderPath)
        logging.info(filesInFolder)
        # print("filesInFolder: ")
        # print(filesInFolder)
        countOfProcessedTxt = functions.createTxtFromJsonOrXml(folderPath)
        # print("szar2")
        logging.info("Number of files processed to TXT file : " + str(countOfProcessedTxt))
        # exit()
        functions.processTxtFilesToDailyFiles(folderPath)
        # quotaToNameDict = addToQuotaList(quotaToNameDict, person, first, last, countMessages)
        txtFiles = list(filter(lambda x: (str(x).endswith('.txt')), filesInFolder))
        logging.info(txtFiles)


#processJsonToTxtAndThenToDayFiles()



# ===========================
# AFTER PROCESSING ALL FOLDER, PRINT TOP LISTS
# with open(FOLDER_GEN_HTML + '\\n' + "doneFile.txt", "w", encoding="utf-8") as doneF:
#     for line in doneFiles:
#         doneF.write('%s\n' % line)
# doneF.close()
#displayQuoteToNameDict(quotaToNameDict)
#displayMostMessagesDict(messageCountToNameDict)

# deletes all the empty folders, that have been generated
def deleteEmptyFolders(pathToGenerated):
    yearDirs = os.listdir(pathToGenerated)
    yearDirs = os.walk(pathToGenerated)
    for x in os.walk(pathToGenerated):
        if not(x[1])  and not(x[2]):
            print(str(x))
            #os.remove(x[0])
            #print(x[0] + " removed.")


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
                numOfLines = int((chat.split("_")[1]).split(".")[0])
                #print(numOfLines)
                sumOfAllLines = numOfLines + sumOfAllLines

            #print("sum of all: " + str(sumOfAllLines))
            if int(day.split("\\")[2]) < 10:
                month = "0" + day.split("\\")[2]
            else:
                month = day.split("\\")[2]

            if int(day.split("\\")[3]) < 10:
                thatDay = "0" + day.split("\\")[3]
            else:
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
    print(sorted_items)
    print(type(sorted_items))

    return dayToCountDict


dayToCount = showFilesInFolders(FOLDER_GEN_HTML)


def analyzeByYearAll(dayToCount):
    print(dayToCount)
    yearToCount = {}
    for date, val in dayToCount.items():
        print(date + " " + str(val))
        year = date.split("-")[0]
        if year in yearToCount:
            yearToCount[year] = yearToCount[year] + val
        else:
            yearToCount[year] = val
    print(yearToCount)

def analyzeByMonthsAll(dayToCount):
    print(dayToCount)
    yearMonthToCount = {}
    for date, val in dayToCount.items():
        #print(date + " " + str(val))
        year = date.split("-")[0]
        month = date.split("-")[1]
        if int(month) < 10:
            yearMonth = year + "0" + month
        else:
            yearMonth = year + month
        if yearMonth in yearMonthToCount:
            yearMonthToCount[yearMonth] = yearMonthToCount[yearMonth] + val
        else:
            yearMonthToCount[yearMonth] = val
    print(yearMonthToCount)


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


def orderedPersonList(orderedPersonList):
    pass


def buildPersonFiles(param):
    pass


buildPersonFiles(getListOfAllPersonsInDayFiles(FOLDER_GEN_HTML))






listOfAllThePersons = getListOfAllPersonsInDayFiles(FOLDER_GEN_HTML)
print(listOfAllThePersons)
print(len(listOfAllThePersons))


def generateSumHtml():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%Hh%Mm%Ss")
    print(dt_string)
    pass

def getPhases():
    PHASES = []
    return PHASES



generateSumHtml()
endTime = time.time()
spentTime = endTime - startingTime
logging.info("Program runned for " + str(spentTime) + " seconds.")
#todo logging system


