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
    yearMonthDay = year + "-" + month + "-" + day

    # if year in dateStat:
    #     recentYear = int(dateStat[year])
    #     dateStat[year] = recentYear + 1
    # else:
    #     dateStat[year] = 1
    if yearMonth in dateStat:
        recentYearMonth = int(dateStat[yearMonth])
        dateStat[yearMonth] = recentYearMonth + 1
    else:
        dateStat[yearMonth] = 1
    # if yearMonthDay in dateStat:
    #     recentYearMonth = int(dateStat[yearMonthDay])
    #     dateStat[yearMonthDay] = recentYearMonth + 1
    # else:
    #     dateStat[yearMonthDay] = 1

    #print("\n")
    #print(dateStat)
    return dateStat


def generateContent(keys, values):
    templateStart = """
    <html>
    <head> 
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js" integrity="sha512-d9xgZrVZpmmQlfonhQUvTR7lMPtO7NkZMkA0ABN3PHCbKA5nqylQ/yWlFAyY6hYgdF1Qh6nYiuADWwKB4C2WSw==" crossorigin="anonymous"></script>
    <title>Template {{ title }}</title>
    </head>
    <body>
    
    """
    templateEnd1 = """
        <script>
        new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: 
        """

    templateEnd2 = """
            ,
        datasets: [{ 
            data: 
            """
    templateEnd3 = """
            ,
            label: "Africa",
            borderColor: "#3e95cd",
            fill: false
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: 'World population per region (in millions)'
        }
      }
    });
            </script>
            </body>
            </html>
            """
    content = templateStart
    content += '<h1> valami </h1><canvas id="line-chart" width="800" height="450"></canvas>'
    content += templateEnd1
    content +=str(list(keys))
    content += templateEnd2
    content += str(list(values))
    content += templateEnd3


    return content


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
            if ((m['sender_name'] == person2) & ("content" in m)):
                print(counter)
                csabauzik = csabauzik + 1
                date = getDate(m['timestamp_ms'])
                print(encodeText(person2) + " " + date + " : ")
                dateStat = processDateStat(dateStat, date)
                datam = m['content']
                print(encodeText(datam))
            if ((m['sender_name'] == person1) & ("content" in m)):
                print(counter)
                date = getDate(m['timestamp_ms'])
                print(encodeText(person1 ) + " " + date + " : ")
                dateStat = processDateStat(dateStat, date)
                datam = m['content']
                print(encodeText(datam))
            counter += 1

        print("\n")
        print("All message : " + str(mess_count))
        print(person2 + str(csabauzik))
        print(person1  + str(mess_count -csabauzik))
        print("First mess : " + getDate(firstMess))
        print("Last mess : " + getDate(lastMess))
        print("Date Stats : ")
        print(dateStat)
        print("ODA")
        dateStatList = list(dateStat.keys())[::-1]
        dateStatKValues = list(dateStat.values())[::-1]
        print(dateStatList)
        print(dateStatKValues)
        htmlFilename = encodeText(person1) + "-" + encodeText(person2) + " " + getDate(firstMess).split()[0] + "---" + getDate(lastMess).split()[0] + "_index.html"
        htmlFilename = htmlFilename.replace(" ", "_")
        print(htmlFilename)
        f = open(htmlFilename, "w")
        content = generateContent(dateStatList, dateStatKValues)
        f.write(content)
        f.close()





#mypath = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail'
mypath2 = 'D:\\_code\\python\\messenger_parser\\'
onlyfiles = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
print(onlyfiles)
for file in onlyfiles:
    print(file)
    if (file.endswith('.json')):
        print("is json")
        processJson(file)