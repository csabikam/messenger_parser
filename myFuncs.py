import json
import os
from datetime import datetime

from readJson import encodeText

GEN_HTML = "generated_html"
SORTED_BY_YEAR = "sorted_by_year"
SORTED_BY_MONTH = "sorted_by_month"

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

def processJsonByDay2(jsonPath):
    print(jsonPath)
    dateStat = {}
    person1Stat = {}
    person2Stat = {}
    with open(jsonPath) as f:
        data = json.load(f)
        names = data['participants']
        if len(names) == 1:
            print("CSAK EGY")
            return 0
        person1 = names[0]["name"]
        person1 = encodeText(person1)
        person2 = names[1]["name"]
        person2 = encodeText(person2)


processJsonByDay2(jsonPath)
print("szar")

# now = datetime.now()
# print(now)
# print(type(now))
# getDateResult = getDateOfNow()
# print("getDate result : " + getDateResult)