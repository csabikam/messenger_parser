from os import listdir
from os.path import isfile, join
import json
import ftfy
from datetime import datetime

mypath2 = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail\\buzaspatrik_b9xc2ct-zq\\'
STRING_VIDA_CSABA = 'Vida Csaba'
STRING_P = 'BuzÃ¡s Patrik'

def getDate(timestamp):
    dt_obj = datetime.fromtimestamp(timestamp / 1000).strftime('%y-%m-%d %H:%M:%S')
    #print(dt_obj)
    return str(dt_obj)

def encodeText(text):
    #print(text)
    return ftfy.ftfy(text)
    #return text.encode('cp1252').decode('utf8')


def processDateStat(dateStat, date):
    #print(dateStat)
    #print("====")
    date = date.split()[0]
    year = date.split("-")[0]
    month = date.split("-")[1]
    day = date.split("-")[2]
    #print(date)
    #print(year)
    #print(month)
    #print(day)
    yearMonth = year + "-" + month

    if year in dateStat:
        recentYear = int(dateStat[year])
        dateStat[year] = recentYear + 1
    else:
        dateStat[year] = 1
    if yearMonth in dateStat:
        recentYearMonth = int(dateStat[yearMonth])
        dateStat[yearMonth] = recentYearMonth + 1
    else:
        dateStat[yearMonth] = 1

    #print("\n")
    #print(dateStat)
    return dateStat

def processJson(file):
    print(file)
    dateStat = {}
    fileName = mypath2 + file
    print(fileName)
    with open(fileName) as f:
        data = json.load(f)
        names = data['participants']
        print("ITT")
        print(names)
        person1 = names[0]["name"]
        person2 = names[1]["name"]
        print(person1)
        print(person2)
        messages = data['messages']
        print(messages)
        mess_count = len(messages)
        print("DArab üzenet " + str(mess_count))
        print(messages[0])
        lastMess = messages[0]['timestamp_ms']
        firstMess = messages[len(messages)-1]['timestamp_ms']
        csabauzik = 0
        counter = 0
        for m in messages:
            print("\n")
            if "content" in m:
                data = m['content']
                #print(data)
                # print(encodeText(data))
                # https://stackoverflow.com/questions/26614323/in-what-world-would-u00c3-u00a9-become-%C3%A9
            if ((m['sender_name'] == STRING_VIDA_CSABA) & ("content" in m)):
                print(counter)
                csabauzik = csabauzik + 1
                print(STRING_VIDA_CSABA + " " + date + " : ")
                dateStat = processDateStat(dateStat, date)
                datam = m['content']
                print(encodeText(datam))
            if ((m['sender_name'] == STRING_P) & ("content" in m)):
                print(counter)
                date = getDate(m['timestamp_ms'])
                print(encodeText(STRING_P ) + " " + date + " : ")
                dateStat = processDateStat(dateStat, date)
                datam = m['content']
                print(encodeText(datam))
            counter += 1

        print("\n")
        print("All message : " + str(mess_count))
        print("Csabauzik " + str(csabauzik))
        print("Patrikuzik "  + str(mess_count -csabauzik))
        print("First mess : " + getDate(firstMess))
        print("Last mess : " + getDate(lastMess))
        print("Date Stats : ")
        print(dateStat)





mypath = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail'
onlyfiles = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
print(onlyfiles)
for file in onlyfiles:
    print(file)
    if (file.endswith('.json')):
        print("is json")
        processJson(file)