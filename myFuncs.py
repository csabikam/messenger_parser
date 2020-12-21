import json
import os
from datetime import datetime

import ftfy

STRING_VIDA_CSABA = 'Vida Csaba'
GEN_HTML = "generated_html"
SORTED_BY_YEAR = "sorted_by_year"
SORTED_BY_MONTH = "sorted_by_month"

def encodeText(text):
    return ftfy.ftfy(text)
    #return text.encode('cp1252').decode('utf8')

def getDateWithTime(timestamp) -> str:
    dt_obj = datetime.fromtimestamp(timestamp / 1000).strftime('%y-%m-%d %H:%M:%S')
    #print(dt_obj)
    return str(dt_obj)

def prepareFolders():
    current_dir = os.getcwd()
    genHtmlDir = current_dir + '\\' + GEN_HTML
    if not os.path.exists(genHtmlDir):
        os.makedirs(genHtmlDir)
    startYear = 2007
    endYear = 2021
    for year in range(startYear, endYear):
        actYear = str(year)
        actYearPath = genHtmlDir + '\\' + actYear
        if not os.path.exists(actYearPath):
            os.makedirs(actYearPath)
        for month in range(1,13):
            actMonth = str(month)
            actMonthPath = actYearPath + '\\' + actMonth
            if not os.path.exists(actMonthPath):
                os.makedirs(actMonthPath)
            for month in range(1, 32):
                actDay = str(month)
                actDayPath = actMonthPath + '\\' + actDay
                if not os.path.exists(actDayPath):
                    os.makedirs(actDayPath)
                    print(actDayPath + ' created.')
                else:
                    print(actDayPath + ' already exists.')


def processFolder(folderName):
    prepareFolders()

def getDateOfNow() -> str:
    dt_obj = datetime.now()
    result = str(dt_obj).split(" ")[0]
    return result


jsonPath = 'd:\\_code\\python\\messenger_parser\\json\\abirlachhab_4uspm46zng\\message_1.json'

def getHtmlFilenameByDay(count, name):
    result = name + "_" + str(count) + ".html"
    return result

def getDay(date):
    day = date.split(" ")[0]
    day = day.split("-")[2]
    return int(day)

def getMonth(date):
    day = date.split(" ")[0]
    day = day.split("-")[1]
    return int(day)

def getYear(date):
    day = date.split(" ")[0]
    day = day.split("-")[0]
    return int(day)


def writeToFile(person, msgList, year, month, day):
    print(person)
    print(msgList)
    print(year)
    print(month)
    print(day)
    exit()
    pass


def processJsonByDay2(jsonPath):
    print(jsonPath)
    dateStat = {}
    person1Stat = {}
    person2Stat = {}
    with open(jsonPath) as f:
        msgContent = json.load(f)
        names = msgContent['participants']
        if len(names) == 1:
            print("CSAK EGY")
            return 0
        person1 = names[0]["name"]
        person1 = encodeText(person1)
        person2 = names[1]["name"]
        person2 = encodeText(person2)
        if person2 == STRING_VIDA_CSABA:
            person = person1
        else:
            person = person2
        messages = msgContent['messages']
        year = ""
        month = ""
        day = ""
        list.reverse(messages)
        print(type(messages))
        counter = 0
        content = ""
        msgList = []
        oldDay = 0
        for message in messages:
            name = encodeText(message['sender_name'])
            fullmessage = ""
            if "content" in message:
                date = getDateWithTime(message['timestamp_ms'])
                counter = counter + 1
                msgContent = encodeText(message['content'])
                name = encodeText(message['sender_name'])
                print(date)
                day = getDay(date)
                print(day)
                #exit()
                if day != oldDay and oldDay != 0:
                    writeToFile(person, msgList, year, month, oldDay)
                    msgList = []
                    counter = 0
                oldDay = day
                year = "20" + str(getYear(date))
                month = getMonth(date)
                nameDateMsg = name + " [20" + date + "]" +  " :" + msgContent
                print(year)
                print(month)
                print(day)
                print(msgContent)
                print(name)
                print(counter)
                print(nameDateMsg)
                print(message)
                print(type(messages))
                msgList.append(str(counter) + ". " + nameDateMsg)
                print(len(msgList))
                print("szar")
        exit()


processJsonByDay2(jsonPath)
print("szar")

# now = datetime.now()
# print(now)
# print(type(now))
# getDateResult = getDateOfNow()
# print("getDate result : " + getDateResult)