import os
import random
import re
from os.path import isfile, join
import json
import ftfy
from datetime import datetime
import unidecode
import time
import logging

#2021-01-09

# CONSTANTS AND PATHS _____START
#pathToFolders = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail\\buzaspatrik_b9xc2ct-zq\\' #abs path in case needed for copying
FOLDER_GEN_HTML = "generated_html"
FOLDER_ABC = "ABC_NAME_TO_DATE"
FOLDER_JSON = "json"
FOLDER_BIG_FILES = "BIG_HTML_FILES"
FOLDER_LOG = "log"
FILE_DONEFILE = "doneFile.txt"
initFoldersList = [FOLDER_JSON, FOLDER_GEN_HTML, FOLDER_ABC, FOLDER_LOG]

STRING_VIDA_CSABA = 'Vida Csaba'
#mypath2 = 'c:\\Users\\abasc\\Documents\\_csaba\\_MYFINALBK_MATERIAL_20201124\\emailezesek\\fb_uzik_jso\\fbextracted\messages\inbox\\'
#mypath = 'C:\\Users\\abasc\\OneDrive\\Desktop\\tempfbtoGmail-20201113T210235Z-001\\tempfbtoGmail'
#mypath2 = 'D:\\_code\\python\\messenger_parser\\'
# CONSTANTS AND PATHS _____END

def getPathInGenHtml(folderName):
    foldernameWithPath = FOLDER_GEN_HTML + '\\' + folderName
    return foldernameWithPath

def getDateWithTime(timestamp) -> str:
    dt_obj = datetime.fromtimestamp(timestamp / 1000).strftime('%y-%m-%d %H:%M:%S')
    #print(dt_obj)
    return "20" + str(dt_obj)

def getDateOfNow() -> str:
    dt_obj = datetime.now()
    result = str(dt_obj).split(" ")[0]
    return result

def encodeText(text):
    return ftfy.ftfy(text)
    #return text.encode('cp1252').decode('utf8')

def processDateStat(dateStat, date):
    date = date.split()[0]
    year = date.split("-")[0]
    month = date.split("-")[1]
    day = date.split("-")[2]
    yearMonth = year + "-" + month
    yearMonthDay = year + "-" + month + "-" + day

    if yearMonth in dateStat:
        recentYearMonth = int(dateStat[yearMonth])
        dateStat[yearMonth] = recentYearMonth + 1
    else:
        dateStat[yearMonth] = 1
    return dateStat

def getScript(dates, allMessageValues, p1MessageValues, p2MessageValues, person1, person2):
    script = """
    <script>
        window.randomScalingFactor = function() {
		return Math.floor(Math.random() * 100); 
	};
		var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var config = {
			type: 'line',
			data: {
				labels: """ + str(list(dates))+ """,
				datasets: [{
					label: 'All messages',
					backgroundColor: '#C21990',
					borderColor: '#C21990',
					data: 
					
					""" + str(list(allMessageValues)) + """
					,
					fill: false,
				},
				 {
					label: ' """  + str(person1) + """ ',
					backgroundColor: '#19B8C2',
					borderColor: '#19B8C2',
					data: 
					""" + str(list(p1MessageValues)) + """,
					fill: false,
				},
				 {
					label: ' """  + str(person2) + """ ',
					fill: false,
					backgroundColor: '#C29919',
					borderColor: '#C29919',
					data: 
					""" + str(list(p2MessageValues)) + """,
				}]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Chart.js Line Chart'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Month'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Value'
						}
					}]
				}
			}
		};

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myLine = new Chart(ctx, config);
		};

		

		var colorNames = Object.keys(window.chartColors);
		document.getElementById('addDataset').addEventListener('click', function() {
			var colorName = colorNames[config.data.datasets.length % colorNames.length];
			var newColor = window.chartColors[colorName];
			var newDataset = {
				label: 'Dataset ' + config.data.datasets.length,
				backgroundColor: newColor,
				borderColor: newColor,
				data: [],
				fill: false
			};

			for (var index = 0; index < config.data.labels.length; ++index) {
				newDataset.data.push(randomScalingFactor());
			}

			config.data.datasets.push(newDataset);
			window.myLine.update();
		});

		

		
		
	</script>
	</body>
                </html>
    """

    scriptStart = """
            <script>
            new Chart(document.getElementById("line-chart"), {
      type: 'line',
      data: {
        labels: 
            """

    dataSetStart = """
                ,
            datasets: ["""
    dataStart =       """{ 
                data: 
                """
    dataSetEnd = """
                ,
                label: "All messages",
                borderColor: "#3eeeee",
                fill: false
              }"""
    scriptEnd ="""]
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
    content = script
    return content

def generateContent(keys, values, data1):
    print(len(data1["messages"]))
    changeList = [ "Newline after day separation should be put",
                   "Extended chart, with 0 months",
                   "Cleaned words, only a-zA-z0-9"

    ]
    name = data1["name"]
    templateStart = """
    <!DOCTYPE html>
    <head lang="hu"> 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
$(document).ready(function(){
  $("button").click(function(){
    console.log("pushed");
    $("#words").toggle();
  });
});
</script>
</head>
<body>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js" integrity="sha512-d9xgZrVZpmmQlfonhQUvTR7lMPtO7NkZMkA0ABN3PHCbKA5nqylQ/yWlFAyY6hYgdF1Qh6nYiuADWwKB4C2WSw==" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
       <title> """  + data1["filename"]+ """</title>
    </head>
    <body>
    <div class="container"> 
    <h1> """ + name + """ </h1>
    <h6> """ + str(changeList) + """ </h6>
    
    </div>
    
    """

    content = templateStart
    stringem = str(data1["first"])
    utso = str(data1["last"])

    lastMessage = "last" in data1
    myMessages = data1["messages"]
    messCount = data1["count"]
    timeDiff = data1["diff"]
    redWords=data1["redWords"]
    words = data1["words"]
    person1 = data1["person1"]
    person2 = data1["person2"]
    #person1Values = data1[person1]
    #person2Values = data1[person2]
    listToStr = ', '.join([str(elem) for elem in redWords])
    #commonWords = nltk.FreqDist(words)
    #collocations = words.collocations()
    #print(collocations)


    #commonWList = commonWords.most_common(250)
    if lastMessage:
        lastM = str(data1["last"])
        #print(lastMessage)
    else:
        lastM = "UNKNOWN"
    content += """ <div class="container">
  <div class="row">
  
    
    <div class="col"><p class="text-danger"> Converstaion of : """ + name + """</p>  </div>
    <div class="col"><p> Msg count: """ + str(messCount) + """</p>  </div>
    <div class="col"><p> Elso uzi: """ + stringem + """</p>  </div>
    <div class="col"><p> Utolso uzi: """ + lastM + """ </p></div>
    <div class="col"><p> Eltelt idŐ: """ + "todo: timeDiff" + """ </p></div>
    <div class="col"> Most common words : """ + "str(commonWList)" + """   </div>
    <div class="col"> <button>Toggle "words"</button> </div>
    
    <div class="col" id="words"> Words :  """ +  str(len(set(words))) + " | " +  str(set(words)) + """ </div>
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
    <div class="col"><canvas id="canvas" width="600" height="500"></canvas></div>"""


    countme = 0
    for mess in myMessages:
        countme += 1
        content += '<div class="col blue">'
        #print(mess)
        content += '<a href="#" class="text-light bg-dark"> ' + str(countme) + " : </a>"
        content += str(mess)
        content += '<div>'

    content += """"
  </div>
</div>
"""
    #print(values)
    allMessages =  values["all"]
    person1Values = values[person1]
    person2Values = values[person2]
    keys.sort()
    content += getScript(keys, allMessages, person1Values, person2Values, person1, person2)
    return content

def processWord(words, toProcess):
    wordUnits = toProcess.split(" ")
    wordUnits = map(lambda x: x.lower(), wordUnits)
    wordUnits = map(lambda x: re.sub('[^A-Za-z0-9]+', '', x), wordUnits)
    #re.sub('[^A-Za-z0-9]+', '', x)
    words.extend(wordUnits)
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(str(toProcess))
    return sorted(words)

def processSumFile(nameOfSumFile, dateStat, data):
    fileName = data["filenameToStore"].split(".html")[0] + "_sum.txt"
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    return 0

def getDay(date):
    day = date.split(" ")[0]
    day = day.split("-")[2]
    return int(day)

def extendChartData(dateStat):
    extendedDates = {'20-05': 63, '19-05': 12, '19-03': 138, '19-02': 44, '19-01': 186, '18-12': 137, '18-11': 33,
                     '18-10': 321, '18-09': 27, '18-07': 2, '18-06': 140, '18-04': 92, '18-03': 138, '18-02': 361,
                     '18-01': 156, '15-07': 380, '15-06': 830}
    #print(extendedDates)
    extendedDates = dateStat
    firstDate = min(extendedDates)
    lastDate = max(extendedDates)
    #print(firstDate)
    #print(lastDate)
    firstYear = int(firstDate.split("-")[0])
    firstMonth = int(firstDate.split("-")[1])
    lastYear = int(lastDate.split("-")[0])
    lastMonth = int(lastDate.split("-")[1])
    months = []

    for x in range(firstYear, lastYear):
        month = ""
        for i in range(1, 13):
            month = ""
            if i < 10:
                month += str(x) + "-" "0"
                month += str(i)
            else:
                month += str(x) + "-" + str(i)
            # print("month : " + month)
            months.append(month)
            # print(months)
            #print("=")

    for month in months:
        #print(month)
        if month in extendedDates:
            pass
        else:
            extendedDates[month] = 0

    #print(extendedDates)
    # print(firstYear)
    # print(firstMonth)
    # print(lastYear)
    # print(lastMonth)

    # for k in extendedDates:
    # print(i)
    # print()

    #
    # ()
    return extendedDates

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

def getHtmlFilename1(name, count, dateFrom, dateTo, format):
    return getHtmlFilename(name, STRING_VIDA_CSABA, count, dateFrom, dateTo, format)

def processJson(jsonFile):
    dateStat = {}
    person1Stat = {}
    person2Stat = {}
    fileName = jsonFile
    print("fileName = " + fileName)
    with open(fileName) as f:
        data = json.load(f)
        names = data['participants']
        if len(names) == 1:
            print("CSAK EGY")
            return 0
        person1 = names[0]["name"]
        person1 = encodeText(person1)
        person2 = names[1]["name"]
        person2 = encodeText(person2)
        messages = data['messages']
        firstMess = messages[len(messages)-1]['timestamp_ms']
        lastMess = messages[0]['timestamp_ms']
        mess_count = len(messages)
        dateFrom = getDateWithTime(firstMess).split()[0]
        dateTo   = getDateWithTime(lastMess).split()[0]
        htmlFilename = getHtmlFilename(person1, person2, mess_count, dateFrom, dateTo, "html")
        sumFilename = getHtmlFilename(person1, person2, mess_count, dateFrom, dateTo, "txt")
        if (os.path.exists(htmlFilename)):
            return 0
        print("DArab üzenet " + str(mess_count))
        print(messages[0])
        timeDiff = lastMess - firstMess
        csabauzik = 0
        counter = 0
        myMessages = []
        #arrayMessages = np.array([])
        words = []
        global lastMessageDay
        lastMessageDay = 0
        for message in messages:
            print("\n")
            name = encodeText(message['sender_name'])
            fullmessage = ""
            if "content" in message:
                data = message['content']
                #print(encodeText(data))

                # https://stackoverflow.com/questions/26614323/in-what-world-would-u00c3-u00a9-become-%C3%A9
            if ((name == person2) & ("content" in message)):
                print(counter)
                csabauzik = csabauzik + 1
                date = getDateWithTime(message['timestamp_ms'])
                lastDay = getDay(date)
                lastDay = lastDay

                if (lastMessageDay != lastDay):
                    #print("elkélne egy")
                    myMessages.append("""
                    ------------------||------------------
                    |""")
                lastMessageDay = lastDay

                messageContent = ""

                #print(encodeText(person2) + " [" + date + "] : ")
                dateStat = processDateStat(dateStat, date)
                person2Stat = processDateStat(person2Stat, date)
                dateStat = extendChartData(dateStat)
                person2Stat = extendChartData(person2Stat)
                messageContent += message['content']
                toProcess = encodeText(messageContent)
                words = processWord(words, toProcess)
                message = encodeText(" [20" + date  + "]" + person2 + " :" + messageContent)
                lastMessageDay = lastDay
                myMessages.append(str(counter) + " " + message)

            if ((name == person1) & ("content" in message)):
                # print(person1)
                # print("BEAA")
                # print(data)
                # print(data)
                # print(name)
                print(counter)
                date = getDateWithTime(message['timestamp_ms'])
                print(encodeText(person1) + " [20" + date + "] : ")
                dateStat = processDateStat(dateStat, date)
                dateStat = extendChartData(dateStat)
                person1Stat = processDateStat(person1Stat, date)
                person1Stat = extendChartData(person1Stat)
                messageContent = message['content']
                #print(encodeText(messageContent))
                day = getDay(date)
                lastMessageDay = int(day)
                toProcess = encodeText(messageContent)
                #
                words = processWord(words, toProcess)
                message = encodeText(person1 + " [20" + date + "] : \n " + messageContent)
                myMessages.append(str(counter) + " " + message)
                #print("==========")
                #print(message)
                #print("__")
            counter += 1


        print("\n")
        print(words)
        print("All message : " + str(mess_count))
        if mess_count < 100:
            return 0
        print(str(person2) + str(csabauzik))
        print(person1  + str(mess_count -csabauzik))
        print("First mess : " + getDateWithTime(firstMess))
        print("Last mess : " + getDateWithTime(lastMess))
        print(dateStat)
        print(dateStat)
        dateStat = extendChartData(dateStat)
        person1Stat = extendChartData(person1Stat)
        person2Stat = extendChartData(person2Stat)
        print(dateStat)
        dateStatList = list(dateStat.keys())[::-1]
        dateStatKValues = list(dateStat.values())[::-1]
        person1Stat = list(person1Stat.values())[::-1]
        person2Stat = list(person2Stat.values())[::-1]
        print(dateStat)
        nameOfSumFile = (person1 + "_" + person2).replace(" ",  "_")
        print(nameOfSumFile)
        values = {}
        values["all"] = dateStatKValues

        values[person1] = person1Stat
        values[person2] = person2Stat

        print(htmlFilename)

        myOrigMessages = list(myMessages)
        myOrigMessages.reverse()


        #print(arrayMessages)
        #print(myOrigMessages)
        #print(myMessages)

        data = {}
        data["person1"] = person1
        data["person2"] = person2
        data["words"] = words
        data["messages"] = myOrigMessages
        data["diff"] =  getDateWithTime(timeDiff)
        data["first"] = getDateWithTime(firstMess)
        data["filename"] = htmlFilename
        redWords = {
            "fasz", "pina", "szex", "szerelem", "mell", "fasz", "here", "golyo", "tökeim", "bimbó"

        }
        redWords = {}

        data["redWords"] = redWords
        print("ide " +  data["first"])

        data["last"] = getDateWithTime(lastMess)
        data["name"] = encodeText(person1 + " - " + person2)
        data["count"] = mess_count
        print(htmlFilename)
        print("ide " + data["last"])
        dataToSumFile = {}
        dataToSumFile["conversationBetween"] = encodeText(name)
        dataToSumFile["thisFileCreatedAt"] =  str(datetime.now())
        dataToSumFile["diff"] = getDateWithTime(timeDiff)
        dataToSumFile["firstMessage"] = getDateWithTime(firstMess)
        dataToSumFile["filenameToStore"] = encodeText(htmlFilename)

        print(htmlFilename)
        #processSumFile(nameOfSumFile, dateStat, dataToSumFile)
        content = generateContent(dateStatList, values, data)


        htmlFilenamePath = getBigHtmlFilesPath() + '\\' +  htmlFilename

        with open(htmlFilenamePath, "w", encoding="utf-8") as f:
            f.write(content)

        f.close()
        print(fileName)
        print(htmlFilename)
        return 1

def getBigHtmlFilesPath():
    current_dir = os.getcwd()
    bigHtmlFilesPath = current_dir + '\\' + FOLDER_GEN_HTML + '\\' + FOLDER_BIG_FILES
    return bigHtmlFilesPath


def processJsonByDay(actualJsonPath):
    dateStat = {}
    person1Stat = {}
    person2Stat = {}
    fileName = actualJsonPath
    print("fileName = " + fileName)
    with open(fileName) as f:
        data = json.load(f)
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
        #if (os.path.exists(htmlFilename)):
           # return 0
        print("DArab üzenet " + str(mess_count))
        print(messages[0])
        timeDiff = lastMess - firstMess
        csabauzik = 0
        counter = 0
        myMessages = []
        # arrayMessages = np.array([])
        words = []
        global lastMessageDay
        lastMessageDay = 0
        for message in messages:
            name = encodeText(message['sender_name'])
            fullmessage = ""
            if "content" in message:
                data = message['content']
                # print(encodeText(data))

                # https://stackoverflow.com/questions/26614323/in-what-world-would-u00c3-u00a9-become-%C3%A9
            if ((name == person2) & ("content" in message)):
                print(counter)
                csabauzik = csabauzik + 1
                date = getDateWithTime(message['timestamp_ms'])
                lastDay = getDay(date)
                lastDay = lastDay

                if (lastMessageDay != lastDay):
                    # print("elkélne egy")
                    myMessages.append("""
                        ------------------||------------------
                        |""")
                lastMessageDay = lastDay
                messageContent = ""

def createClearJson(fileName, htmlFileName, abcDaysFile):
    print()
    print("Processing " + fileName)
    htmlFileNameWithPath = os.path.dirname(fileName) + "\\" + htmlFileName
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

def getNumberOfDays(first, last):
    if (first != "") & (last != "") :
        startYear = first.split()[0].split("-")[0]
        lastYear = last.split()[0].split("-")[0]
        startMonth = first.split()[0].split("-")[1]
        lastMonth = last.split()[0].split("-")[1]
        startDay = first.split()[0].split("-")[2]
        lastDay = last.split()[0].split("-")[2]
        yearDiff = int(lastYear) - int(startYear)
        monthDiff = int(lastMonth)- int(startMonth)
        dayDiff = int(lastDay) - int(startDay)
        numberOfDays = yearDiff * 365 + monthDiff * 30 + dayDiff
        #print(dayDiff)
        #print(numberOfDays)
        return numberOfDays
    else:
        return 0


def createAbcFile(abcDaysFile, person):
    print(type(abcDaysFile))
    print(abcDaysFile)
    if len(abcDaysFile) == 0:
        return []
    lastName = person.split()[-1]
    letter = lastName[0].capitalize()
    abcPath = FOLDER_ABC
    if not os.path.exists(abcPath):
        os.mkdir(abcPath)
    letterPath = abcPath + '\\' + letter
    if not os.path.exists(letterPath):
        os.mkdir(letterPath)
    person = unidecode.unidecode(person.replace(" ",""))
    filename = person + ".txt"
    filenamePath =  letterPath + '\\'  + filename
    with open(filenamePath, "w", encoding="utf-8") as newFile:
        for recentDate in abcDaysFile:
            newFile.write(recentDate)
            newFile.write('\n')
    newFile.close()

def createSumTxtFileFromJsonFromFolder(folderPath, fileCounter, doneFiles):
    filesOrFoldersInFolder = os.listdir(folderPath)
    jsonFiles = list(filter(lambda x: (str(x).endswith('.json')), filesOrFoldersInFolder))
    countMessages = 0
    person = ""
    first = ""
    last = ""
    abcDaysFile = []
    for file in jsonFiles:
        file = folderPath + '\\' + file
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
            countMessages += countRecentFile
            lastIndex = len(data['messages']) - 1
            firstMessageTime = getDateWithTime(data['messages'][lastIndex]["timestamp_ms"])
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

            ret = createClearJson(file, htmlFileName, abcDaysFile)
            print(abcDaysFile)
            doneFiles.append(file)
            print("Person processed count : " + str(fileCounter))
            fileCounter += 1
    print(person)
    if abcDaysFile:
        print(abcDaysFile)

    createAbcFile(abcDaysFile, person)
    print("Üzenetek száma: " + str(countMessages))
    print("First mess: " + first)
    print("Last mess: " + last)
    return first, last, person, countMessages, fileCounter, False, doneFiles

def addToQuotaList(quotaToNameDict, person, first, last, countMessages):
    numberOfDaysTalked = getNumberOfDays(first, last)
    if numberOfDaysTalked == 0:
        numberOfDaysTalked = 1
    kvota = countMessages / numberOfDaysTalked
    kvota = float("{:.3f}".format(kvota))
    if numberOfDaysTalked > 100:
        quotaToNameDict[kvota] = person + " " + str(numberOfDaysTalked) + " days, " + str(countMessages) + " messages"
        messageCountToNameDict[countMessages] = person + " msgs: " + str(countMessages)
    print("Quta mess/days : Napi üzik : " + str(kvota))
    return quotaToNameDict

def displayQuoteToNameDict(quotaToNameDict):
    print(" ============= LIST OF QUOTE (daysInConnection/messages) =================")
    counter = 1
    for key in sorted(quotaToNameDict, reverse=True):
        print(" ")
        print(counter)
        counter += 1
        print("%s: %s" % (key, quotaToNameDict[key]))
    print(" ============= END OF LIST OF QUOTE (daysInConnection/messages) =================")

def displayMostMessagesDict(messageCountToNameDict):
    print(" ============= LIST OF MessageCount::Name  =================")
    counter = 1
    for key in sorted(messageCountToNameDict, reverse=True):
        print(" ")
        print(counter)
        counter += 1
        print("%s: %s" % (key, messageCountToNameDict[key]))
    print(" ============= END OF LIST OF MessageCount::Name  =================")

def processFolder(folderName):
    print("Starting to process folder: " + folderName)
    dirsToProcess = os.listdir(FOLDER_JSON)
    print("Number of folders : " + str(len(dirsToProcess)))
    print("looking in dirs : " + str(dirsToProcess))
    for dir in dirsToProcess:
        actualPath = FOLDER_JSON + '\\' + dir
        if os.path.exists(actualPath):
            print(actualPath + " exists")
            filesToProcess = os.listdir(actualPath)
            #print(filesToProcess)
            filesToProcess = list(filter(lambda x: (str(x).endswith(".json")), filesToProcess))
            print(filesToProcess)
            for file in filesToProcess:
                actualJsonPath = actualPath + '\\' + file
                with open(actualJsonPath) as json_file:
                    data = json.load(json_file)
                    htmlFileName = getHtmlFileNameFromData(data)
                    htmlFilePath = getBigHtmlFilesPath() + '\\' + htmlFileName
                    print(htmlFileName)
                    if not os.path.exists(htmlFilePath):
                        processJson(actualJsonPath)
                        processJsonByDay(actualJsonPath)
                pass

# STARTING PROGRAM HERE
#processFolder(pathToJsons)

def initFolders(initFoldersList):
    for foldername in initFoldersList:
        if not os.path.exists(foldername):
            os.mkdir(foldername)
            logging.info("Creating folder ( initFolder()) : " + foldername)
        else:
            logging.info("Creating folder ( initFolder()) : " + foldername + " not neccessary. It already exists.")


initFolders(initFoldersList) # generated_html, log, json, abc
startingTime = time.time()


def getDoneFiles():
    file = FOLDER_GEN_HTML + '\\' +  FILE_DONEFILE
    doneFilesList = []
    if os.path.exists(file):
        with open(file, 'r', encoding="utf-8") as reader:
            for line in reader.readlines():
                line = line. rstrip('\n')
                doneFilesList.append(line)
    else:
        return []
    return doneFilesList


filesAlreadyDone = getDoneFiles()
now = datetime.now()
dt_string = now.strftime("%Y%m%d_%Hh%Mm%Ss")
loggingFileName = "logfile_" + dt_string + ".log"
#f= open(loggingFileName,"x")
#f.close()
logging.basicConfig(filename="log" + loggingFileName, encoding='utf-8', level=logging.DEBUG)
dirsToProcessInJsonFolder = os.listdir(FOLDER_JSON)
logging.info("looking in dirs : " + str(dirsToProcessInJsonFolder))
counter = 0
fileCounter = 0
quotaToNameDict = {}
messageCountToNameDict = {}
diagramDataDict = {}

def createDailyFileFromName(person):
    fileName = person + ".day"
    fileName = unidecode.unidecode(encodeText(fileName))
    fileName = fileName.replace(" ", "")
    return fileName


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

def processTxtFilesToDailyFiles(folderPath, person):
    filesOrFoldersInFolder = os.listdir(folderPath)
    txtFiles = list(filter(lambda x: (str(x).endswith('.txt')), filesOrFoldersInFolder))
    print(person)
    fileName = createDailyFileFromName(person)
    print(fileName)
    for actualTxt in txtFiles:
        file = folderPath + '\\' + actualTxt
        print(file)
        if os.path.exists(file):
            print("exists")
        linesToDayFile = []
        tempRecentDate = ""
        fileCounter = 0
        with open(file, 'r', encoding="utf-8") as reader:
            for line in reader.readlines():
                if (line.startswith("200") or line.startswith("201")) and line[4] == '-':
                    recentDate = line.split()[0]
                    if tempRecentDate == "":
                        tempRecentDate = recentDate
                    print(tempRecentDate)
                    yearPath = createYearPath(tempRecentDate)
                    print(yearPath)
                    if not os.path.exists(yearPath):
                        os.mkdir(yearPath)
                        logging.info("Creating " + yearPath)
                    monthPath = createMonthPath(tempRecentDate)
                    print(monthPath)
                    if os.path.exists(monthPath):
                        pass
                    else:
                        os.mkdir(monthPath)
                        logging.info("Creating " + monthPath)
                    dayPath = createDayPath(tempRecentDate)
                    print(dayPath)
                    if os.path.exists(dayPath):
                        pass
                    else:
                        os.mkdir(dayPath)
                        logging.info("Creating " + dayPath)
                    datedPath = createDatePath(tempRecentDate)
                    datedPathAndFilename = datedPath + fileName
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
                            logging.info("File exists already : " + datedPathAndFilename)
                        linesToDayFile = []

                    tempRecentDate = recentDate
                    linesToDayFile.append(line)

for folder in dirsToProcessInJsonFolder:
    logging.info("Start processing " + folder)
    folderPath = FOLDER_JSON + '\\' + folder
    print(folderPath)

    logging.info("Path to this folder "  + folderPath)
    filesOrFoldersInFolder = os.listdir(folderPath)
    print(filesOrFoldersInFolder)
    logging.info("Files in: " + folderPath)
    logging.info(filesOrFoldersInFolder)
    first, last, person, countMessages, fileCounter, alreadyDone, doneFiles = createSumTxtFileFromJsonFromFolder(folderPath, fileCounter, filesAlreadyDone)
    if alreadyDone:
        continue
    processTxtFilesToDailyFiles(folderPath, person)
    logging.info("Conversation with: " + person)
    logging.info("Number of messages: " + str(countMessages))
    logging.info("First conversation  at: " + first)
    logging.info("Last conversation started at: " + last)
    logging.info(str(fileCounter) + ".th processed file")
    logging.info("Starting ")
    quotaToNameDict = addToQuotaList(quotaToNameDict, person, first, last, countMessages)
    txtFiles = list(filter(lambda x: (str(x).endswith('.txt')), filesOrFoldersInFolder))
    logging.info(txtFiles)
    print("\n")
# AFTER PROCESSING ALL FOLDER, PRINT TOP LISTS
with open(FOLDER_GEN_HTML + '\\n' + "doneFile.txt", "w", encoding="utf-8") as doneF:
    for line in doneFiles:
        doneF.write('%s\n' % line)
doneF.close()
displayQuoteToNameDict(quotaToNameDict)
displayMostMessagesDict(messageCountToNameDict)


def generateSumHtml():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%Hh%Mm%Ss")
    print(dt_string)
    pass



generateSumHtml()
endTime = time.time()
spentTime = endTime - startingTime
logging.info("Program runned for " + str(spentTime) + " seconds.")
#todo logging system


