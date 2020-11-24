import os
from os.path import isfile, join
import json
import ftfy
from datetime import datetime
import io

mypath2 = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail\\buzaspatrik_b9xc2ct-zq\\'

STRING_VIDA_CSABA = 'Vida Csaba'

def getDate(timestamp) -> str:
    dt_obj = datetime.fromtimestamp(timestamp / 1000).strftime('%y-%m-%d %H:%M:%S')
    #print(dt_obj)
    return str(dt_obj)

def encodeText(text):
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


def generateContent(keys, values, data1):
    print(data1)
    print(len(data1["messages"]))
    #exit()
    templateStart = """
    <!DOCTYPE html>
    <head> 
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js" integrity="sha512-d9xgZrVZpmmQlfonhQUvTR7lMPtO7NkZMkA0ABN3PHCbKA5nqylQ/yWlFAyY6hYgdF1Qh6nYiuADWwKB4C2WSw==" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style type="text/css">
   
</style>
    <title>Template {{ title }}</title>
    </head>
    <body>
    <div class="container"> 
    <h1> FIRST </h1>
    </div>
    
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
    print(data1["first"] )
    print(data1["last"] )
    stringem = str(data1["first"])
    utso = str(data1["last"])
    name = data1["name"]
    lastMessage = "last" in data1
    myMessages = data1["messages"]
    messCount = data1["count"]
    timeDiff = data1["diff"]
    redWords=data1["redWords"]
    words = data1["words"]
    listToStr = ', '.join([str(elem) for elem in redWords])
    if lastMessage:
        lastM = str(data1["last"])
        print(lastMessage)
    else:
        lastM = "UNKNOWN"
    content += """ <div class="container">
  <div class="row">
  
    
    <div class="col"><p class="text-danger"> Person: """ + name + """</p>  </div>
    <div class="col"><p> Msg count: """ + str(messCount) + """</p>  </div>
    <div class="col"><p> Elso uzi: """ + stringem + """</p>  </div>
    <div class="col"><p> Utolso uzi: """ + lastM + """ </p></div>
    <div class="col"><p> Eltelt idŐ: """ + timeDiff + """ </p></div>
    <div class="col"> Piros szavak: """ + listToStr + """ </div>
     <div class="col"> Words :  """ +  str(len(words)) + " | " +  str(words) + """ </div>
    <div class="w-100"><table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table></div>
    <div class="col">Column</div>
    <div class="col"><canvas id="line-chart" width="auto" height="auto"></canvas></div>"""

    for id, mess in myMessages.items():
        content += '<div class="col"><p>'
        print(mess)
        content += '<a href="#" class="text-light bg-dark"> ' + str(id) + " : </a>"
        content += mess
        content += '</p><div>'


    #exit()

    content += """"
  </div>
</div>
"""
    content += templateEnd1
    content +=str(list(keys))
    content += templateEnd2
    content += str(list(values))
    content += templateEnd3


    return content


def processWord(words, toProcess):
    print(words)
    wordUnits = toProcess.split(" ")
    words.extend(wordUnits)

    print(wordUnits)
    ##print(words)
    print("ANYÁD")
    return sorted(set(words))


def processJson(file):
    print(file)
    dateStat = {}
    fileName = file
    print("fileName = "  + fileName)
    print(fileName)
    with open(fileName) as f:
        data = json.load(f)

        names = data['participants']
        if len(names) == 1:
            print("CSAK EGY")
            return 0
        print("ITT")
        print(data)
        print(names)

        person1 = names[0]["name"]
        person2 = names[1]["name"]
        messages = data['messages']
        firstMess = messages[len(messages)-1]['timestamp_ms']
        lastMess = messages[0]['timestamp_ms']
        htmlFilename = encodeText(person1) + "-" + encodeText(person2) + " " + getDate(firstMess).split()[0] + "---" + \
                       getDate(lastMess).split()[0] + "_index.html"
        htmlFilename = htmlFilename.replace(" ", "_")
        print(htmlFilename)
        if (os.path.exists(htmlFilename)):
            return 0
        print(person1)
        print(person2)
         #print(messages)
        mess_count = len(messages)
        print("DArab üzenet " + str(mess_count))
        print(messages[0])
        timeDiff = lastMess - firstMess
        csabauzik = 0
        counter = 0
        myMessages = {}
        words = []
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

                toProcess = encodeText(datam)
                #
                words = processWord(words, toProcess)
                message = encodeText(person2 + " " + date + " : \n " + datam)
                myMessages[counter] = message
            if ((m['sender_name'] == person1) & ("content" in m)):
                print(counter)
                date = getDate(m['timestamp_ms'])
                print(encodeText(person1 ) + " " + date + " : ")
                dateStat = processDateStat(dateStat, date)
                datam = m['content']
                #print(encodeText(datam))
                toProcess = encodeText(datam)
                #
                words = processWord(words, toProcess)
                message = encodeText(person1 + " " + date + " : \n " + datam)
                myMessages[counter] = message
            counter += 1


        print("\n")
        print(words)
        print("All message : " + str(mess_count))
        if mess_count < 200:
            return 0
        print(str(person2) + str(csabauzik))
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
        print("___DEBUG___")
        print(person1)
        print(person2)
        print("___DEBUG___")
        print(htmlFilename)


        data = {}
        data["words"] = words
        data["person1"] = 1
        data["messages"] = myMessages
        data["diff"] =  getDate(timeDiff)
        data["first"] = getDate(firstMess)
        redWords = {
            "fasz", "pina", "szex", "szerelem", "mell", "fasz", "here", "golyo", "tökeim", "bimbó"

        }

        data["redWords"] = redWords
        print("ide " +  data["first"])

        data["last"] = getDate(lastMess)
        data["name"] = encodeText(person1 + " - " + person2)
        data["count"] = mess_count
        print(htmlFilename)
        print("ide " + data["last"])
        content = generateContent(dateStatList, dateStatKValues, data)

        with open(htmlFilename, "w", encoding="utf-8") as f:
            f.write(content)

        #print(content)
        #exit()
        f.close()
        print(fileName)
        print(htmlFilename)
        return 1





mypath2 = 'c:\\Users\\abasc\\Documents\\_csaba\\_MYFINALBK_MATERIAL_20201124\\emailezesek\\fb_uzik_jso\\fbextracted\messages\inbox\\'
#mypath = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail'
#mypath2 = 'D:\\_code\\python\\messenger_parser\\'
onlyfiles = [f for f in os.listdir(mypath2) if isfile(join(mypath2, f))]
onlyDirs = os.listdir(mypath2)
print(onlyDirs)

print("szar")
for file in onlyfiles:
    print(file)
    if (file.endswith('.json')):
        print("is json")
        processJson(file)
counter = 0
fileCounter = 0
for file in onlyDirs:
    path =mypath2 + file + "\message_1.json"

    with open(path) as json_file:
        print(counter)
        counter += 1
        print(json_file)
        data = json.load(json_file)
        for p in data['participants']:
             print('Name: ' + encodeText(p['name']))
        #     print('Website: ' + p['website'])
        #     print('From: ' + p['from'])
        #     print('')
        print("Üzenetek száma: " + str(len(data['messages'])))

        last = len(data['messages'])-1

        print("Első üzi: " + getDate(data['messages'][last]["timestamp_ms"]))
        print("Utolsó üzi : " + getDate(data['messages'][0]["timestamp_ms"]))
    #exit(0)
    print("\n")

    fileCounter += processJson(path)
    if fileCounter == 1:
        exit()
