import datetime
import os
import random
import re
import xml

import functions
from os.path import isfile, join

import xmltodict

import json
import ftfy
from datetime import datetime
import unidecode
import time
import logging

FOLDER_GEN_HTML = "generated_html"
FOLDER_ABC = "ABC_NAME_TO_DATE"
FOLDER_JSON = "json"
FOLDER_BIG_FILES = "BIG_HTML_FILES"
FOLDER_LOG = "log"
FILE_DONEFILE = "doneFile.txt"
XMLS_TO_TXT = "_txt_from_XML"
initFoldersList = [FOLDER_JSON, FOLDER_GEN_HTML, FOLDER_ABC, FOLDER_LOG]
STRING_VIDA_CSABA = 'Vida Csaba'
doneFiles = []

def initFolders(initFoldersList):
    for foldername in initFoldersList:
        if not os.path.exists(foldername):
            os.mkdir(foldername)
            logging.info("Creating folder ( initFolder()) : " + foldername)
        else:
            logging.info("Creating folder ( initFolder()) : " + foldername + " not neccessary. It already exists.")

def fromFunctions(szar):
    print(szar)

def getDateWithTime(timestamp) -> str:
    print(timestamp)
    dt_obj = datetime.fromtimestamp(timestamp / 1000).strftime('%y-%m-%d %H:%M:%S')
    print(dt_obj)
    return "20" + str(dt_obj)

def processJson(file):
    person = ""
    first = ""
    last = ""
    print("=========================")
    abcDaysFile = []
    print(file)
    print(doneFiles)
    if file in doneFiles:
        print(file + " already has been processed.")
        logging.info(file + " already has been processed.")
        return "", "", "", 0, 0, True, doneFiles
    with open(file) as json_file:

        # print(file.split('\\')[-1])
        data = json.load(json_file)
        for p in data['participants']:
            p = encodeText(p['name'])
            if p == STRING_VIDA_CSABA:
                continue
            else:
                person = p
        countRecentFile = len(data['messages'])
        lastIndex = len(data['messages']) - 1
        firstMessageTime = functions.getDateWithTime(data['messages'][lastIndex]["timestamp_ms"])
        dateFrom = firstMessageTime.split()[0]
        # print("firstm " + firstMessageTime)
        lastMessageTime = getDateWithTime(data['messages'][0]["timestamp_ms"])
        dateTo = lastMessageTime.split()[0]
        # print("lastm " + lastMessageTime)
        if first == "":
            first = firstMessageTime
        else:
            if first > firstMessageTime:
                first = firstMessageTime
        if last == "":
            last = lastMessageTime
        else:
            # print("last "  + last)
            # print("lastMessage "  + lastMessageTime)
            if last < lastMessageTime:
                last = lastMessageTime
        htmlFileName = getHtmlFilename1(person, countRecentFile, dateFrom, dateTo, 'txt')
        print(abcDaysFile)
        #exit()
        print("asda")
        print(file)
        print(htmlFileName)

        ret = createClearJson(file, htmlFileName, abcDaysFile)
        print("fos")
        doneFiles.append(file)

def createTxtFromJsonOrXml(folderPath):

    filesOrFoldersInFolder = os.listdir(folderPath)
    jsonFiles = list(filter(lambda x: (str(x).endswith('.json')), filesOrFoldersInFolder))
    xmlFiles = list(filter(lambda x: (str(x).endswith('.xml')), filesOrFoldersInFolder))
    logging.info("List of json files "  + str(jsonFiles))
    logging.info("List of xml files "  + str(xmlFiles))
    print("List of json files "  + str(jsonFiles))
    print("List of xml files "  + str(xmlFiles))
    counter = 0
    if jsonFiles != []:
        logging.info("Json files : "  + str(jsonFiles))
        for file in jsonFiles:
            file = folderPath + '/' + file
            # volt: counter = counter +
            processJson(file)
            print("hugy")
    if xmlFiles != []:
        logging.info("Xml files : "  + str(jsonFiles))
        for file in xmlFiles:
            file = folderPath + '/' + file
            counter += processXml(file)
    return counter
    #start of xml


    setDoneFiles(doneFiles)
    #end of xml

    # if abcDaysFile:
    #     print(abcDaysFile)
    #
    # createAbcFile(abcDaysFile, person)

def getHtmlFileNameFromData(data):
    names = data['participants']
    if len(names) == 1:
        print("CSAK EGY")
        return 0
    person1 = names[0]["name"]
    person1 = encodeText(person1)
    person2 = names[1]["name"]
    person2 = encodeText(person2)
    messages = data['messages']
    firstMess = messages[len(messages) - 1]['timestamp_ms']
    lastMess = messages[0]['timestamp_ms']
    mess_count = len(messages)
    dateFrom = getDateWithTime(firstMess).split()[0]
    dateTo = getDateWithTime(lastMess).split()[0]
    htmlFilename = getHtmlFilename(person1, person2, mess_count, dateFrom, dateTo, "html")
    sumFilename = getHtmlFilename(person1, person2, mess_count, dateFrom, dateTo, "txt")
    return htmlFilename

def encodeText(text):
    return ftfy.ftfy(text)
    #return text.encode('cp1252').decode('utf8')

def getHtmlFilename1(name, count, dateFrom, dateTo, format):
    return getHtmlFilename(name, STRING_VIDA_CSABA, count, dateFrom, dateTo, format)

def getHtmlFilename(name1, name2, count, dateFrom, dateTo, format):
    name = ""
    now = getDateOfNow()
    if name1 == STRING_VIDA_CSABA:
        name = name2
    else:
        name = name1
    if count % 1000 == 0:
        c = str(int(count / 1000)) + 'k'
    else:
        c = str(count)
    name = unidecode.unidecode(encodeText(name))
    name = name.replace(" ", "")
    htmlFilename = "[" + dateFrom + "---" + dateTo + "]_" +str(c) + "__" + name + "." + format
    return htmlFilename

def getDateOfNow() -> str:
    dt_obj = datetime.now()
    result = str(dt_obj).split(" ")[0]
    return result

def createClearJson(fileName, htmlFileName, abcDaysFile):
    print()
    print("Processing " + fileName)
    htmlFileNameWithPath = os.path.dirname(fileName) + "/" + htmlFileName
    print(htmlFileNameWithPath)
    if os.path.exists(htmlFileNameWithPath):
        print("Already exists, returning. File:  " + htmlFileName)
        return []
    print(htmlFileNameWithPath)
    print(htmlFileName)
    print()
    jsonData = {}
    with open(fileName) as f:
        data = json.load(f)
        messages = data['messages']
        if (os.path.exists(htmlFileName)):
            return []
        counter = 0
        for message in messages:
            name = encodeText(message['sender_name'])
            if "content" in message:
                msg = encodeText(message['content'])
                #print(msg)
                # https://stackoverflow.com/questions/26614323/in-what-world-would-u00c3-u00a9-become-%C3%A9
                date = getDateWithTime(message['timestamp_ms'])
                if date in abcDaysFile:
                    pass
                else:
                    abcDaysFile.append(date)
                #print(date)
                jsonData[date] = name + ": "+ msg
    res = dict(reversed(list(jsonData.items())))
    #print(res)
    with open(htmlFileNameWithPath, "w", encoding="utf-8") as newFile:
        for i in res.keys():
            newFile.write(i + " " + res.get(i))
            newFile.write('\n')
    newFile.close()
    print("Generating file " + htmlFileName)
    return abcDaysFile

def getMsgLine(dateAndTime, name, msg):
    result = ""
    if isinstance(msg, str):
        result = dateAndTime + " " + "[" + name + "]" + " : " +  msg
    return result

def processXml(file):
    person = (file.split("\\")[-1]).split(".")[0]
    person = person.split(" ")[0]
    print("Xml processing : " + file)
    print("For person " + person)
    doneFiles = getDoneFiles()
    print(doneFiles)
    exit()
    abcDaysFile = []
    countMessages = 0
    if file in doneFiles:
        logging.info(file + " already has been processed.")
        return 0
    with open(file, 'r', encoding="utf-8") as myfile:
        try:
            obj = xmltodict.parse(myfile.read())
        except xml.parsers.expat.ExpatError as err:
            print("Expaterror ".format(err))
            return 0
        except ValueError:
            print("Could not convert data to an integer.")
            return 0
        except:
            print("Unexpected error:")
            return 0
    #print(json.dumps(obj["Log"]["Message"]))
    if "Log" in obj:
        msgList = obj["Log"]["Message"]
    else:
        #print(obj)
        return 0
    countRecentFile = len(msgList)
    # print(countRecentFile)
    # print(type(msgList))
    # print(msgList)
    if 0 in msgList:
        dateFrom = msgList[0]['@Date'].replace(".","")
        dateTo = msgList[-1]['@Date'].replace(".","")
    else:
        return 0
    counter = 0
    htmlFileName = getHtmlFilename1(person, countRecentFile, dateFrom, dateTo, 'txt')
    htmlFileNameWithPath = os.path.dirname(file) + "\\" + htmlFileName
    logging.info("Processing " + htmlFileName)
    print(htmlFileNameWithPath)
    print(doneFiles)


    with open(htmlFileNameWithPath, "w", encoding="utf-8") as newFile:
        for msg in msgList:
            counter += 1
            dateAndTime = msg["@Date"] + " " + msg["@Time"]
            dateAndTime = (str(dateAndTime)).replace(".", "-")
            dateAndTime = dateAndTime[:10] + dateAndTime[11:]
            name = msg['From']['User']['@FriendlyName']
            if len(name) > 20 :
                name = name[0:20]
            if "#text" in msg['Text']:
                text = msg['Text']['#text']
            else:
                text = msg['Text']
            newFile.write(getMsgLine(dateAndTime, name, text))
            newFile.write('\n')
    newFile.close()

    doneFiles.append(htmlFileName)
    print(countRecentFile)
    print("============")
    return 1
    #ret = createClearJson(file, htmlFileName, "")
    #doneFiles.append(file)

def setDoneFiles(doneFiles):
    return
    if os.path.exists(FILE_DONEFILE):
        with open(FILE_DONEFILE, 'w', encoding="utf-8") as reader:
            for line in doneFiles:
                reader.write(line)
                reader.write("\n")
        reader.close()
    return

def getPersonnameFromTxtFile(txtFile):
    personName = txtFile.split("__")[1].split(".")[0]
    limit = len(personName)-0
    personName = personName[:limit]
    print(personName)
    return personName

def createDatePath(recentDate):
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        month = str(int(recentDate.split("-")[1]))
        day = str(int(recentDate.split("-")[2]))
        result = FOLDER_GEN_HTML + '\\' + year + '\\' + month + '\\' + day + '\\'
        return result
    else:
        return False

def createYearPath(recentDate):
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        result = FOLDER_GEN_HTML + '\\' + year + '\\'
        return result
    else:
        return False

def createMonthPath(recentDate):
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        month = str(int(recentDate.split("-")[1]))
        result = FOLDER_GEN_HTML + '\\' + year + '\\' + month + '\\'
        return result
    else:
        return False

def createDayPath(recentDate):
    print(recentDate)
    if len(recentDate.split("-")) == 3:
        year = recentDate.split("-")[0]
        month = str(int(recentDate.split("-")[1]))
        day = str(int(recentDate.split("-")[2]))
        result = FOLDER_GEN_HTML + '\\' + year + '\\' + month + '\\' + day + '\\'
        return result
    else:
        return False


def createDailyFileFromNameWithCount(person, countInString):
    print(len(person))
    if person == "":
        return ""
    fileName = person + "_" + countInString + ".day"
    fileName = unidecode.unidecode(encodeText(fileName))
    fileName = fileName.replace(" ", "")
    return fileName


def processTxtFilesToDailyFiles(folderPath):
    filesOrFoldersInFolder = os.listdir(folderPath)
    txtFiles = list(filter(lambda x: (str(x).endswith('.txt')), filesOrFoldersInFolder))

    counter = 0
    for actualTxt in txtFiles:
        file = folderPath + '\\' + actualTxt
        person = getPersonnameFromTxtFile(actualTxt)
        fileName = createDailyFileFromName(person)
        if os.path.exists(file):
            print("exists")
        linesToDayFile = []
        tempRecentDate = ""
        fileCounter = 0
        with open(file, 'r', encoding="utf-8") as reader:
            logging.info(" ")
            logging.info(str(counter) + ".th file : " + file)
            counter += 1
            for line in reader.readlines():
                # todo here 2021 05 07
                if re.match(r'^\d{4}-\d?\d-\d?\d (?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]', line):
                    recentDate = line.split()[0]
                    if tempRecentDate == "":
                        tempRecentDate = recentDate
                    print(tempRecentDate)
                    yearPath = createYearPath(tempRecentDate)
                    print(yearPath)
                    if not os.path.exists(yearPath):
                        os.mkdir(yearPath)
                        #logging.info("Creating " + yearPath)
                    monthPath = createMonthPath(tempRecentDate)
                    print(monthPath)
                    if os.path.exists(monthPath):
                        pass
                    else:
                        os.mkdir(monthPath)
                        #logging.info("Creating " + monthPath)
                    dayPath = createDayPath(tempRecentDate)
                    print(dayPath)
                    if os.path.exists(dayPath):
                        pass
                    else:
                        os.mkdir(dayPath)
                        #logging.info("Creating " + dayPath)
                    datedPath = createDatePath(tempRecentDate)
                    fileNameWithCount = createDailyFileFromNameWithCount(person, str(len(linesToDayFile)))
                    datedPathAndFilename = datedPath + fileNameWithCount
                    print(datedPathAndFilename)
                    if (recentDate != tempRecentDate) & (tempRecentDate != ""):
                        print(linesToDayFile)
                        print(datedPathAndFilename)
                        print(recentDate)
                        if not os.path.exists(datedPathAndFilename):
                            with open(datedPathAndFilename, "w", encoding="utf-8") as newFile:
                                newFile.write("Message count:" + str(len(linesToDayFile)))
                                newFile.write("\n")
                                for i in linesToDayFile:
                                    newFile.write(i)
                            newFile.close()
                            logging.info(str(fileCounter) + "Creating file : " + datedPathAndFilename)
                            fileCounter += 1
                        else:
                            #logging.info("File exists already : " + datedPathAndFilename)
                            pass
                        linesToDayFile = []

                    tempRecentDate = recentDate
                    linesToDayFile.append(line)
                    print("wer")
    logging.info(str(counter) + " files processed.")

def createDailyFileFromName(person):
    print(len(person))
    if person == "":
        return ""
    fileName = person + ".day"
    fileName = unidecode.unidecode(encodeText(fileName))
    fileName = fileName.replace(" ", "")
    return fileName

def processSumFile(nameOfSumFile, dateStat, data):
    fileName = data["filenameToStore"].split(".html")[0] + "_sum.txt"
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    return 0

def getDoneFiles():
    file = FILE_DONEFILE
    doneFilesList = []
    if os.path.exists(file):
        with open(file, 'r', encoding="utf-8") as reader:
            for line in reader.readlines():
                line = line. rstrip('\n')
                doneFilesList.append(line)
    else:
        doneFilePath = FILE_DONEFILE
        with open(doneFilePath, 'w') as fp:
            pass
        return []
    return doneFilesList