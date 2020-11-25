import os
import random
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

    if yearMonth in dateStat:
        recentYearMonth = int(dateStat[yearMonth])
        dateStat[yearMonth] = recentYearMonth + 1
    else:
        dateStat[yearMonth] = 1
    return dateStat


def getScript(dates, allMessageValues, p1MessageValues, p2MessageValues, person1, person2):
    # print("eleje")
    # print(allMessageValues)
    # print(p1MessageValues)
    # print(p2MessageValues)
    # print(person1)
    # print(person2)
    #exit()
    # ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    # [
    # 	randomScalingFactor(),
    # 	randomScalingFactor(),
    # 	randomScalingFactor(),
    # 	randomScalingFactor(),
    # 	randomScalingFactor(),
    # 	randomScalingFactor(),
    # 	randomScalingFactor()
    # ]

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
    #print(data1["messages"])
    #exit()
    templateStart = """
    <!DOCTYPE html>
    <head lang="hu"> 
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js" integrity="sha512-d9xgZrVZpmmQlfonhQUvTR7lMPtO7NkZMkA0ABN3PHCbKA5nqylQ/yWlFAyY6hYgdF1Qh6nYiuADWwKB4C2WSw==" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
       <title>Template {{ title }}</title>
    </head>
    <body>
    <div class="container"> 
    <h1> FIRST </h1>
    </div>
    
    """

    content = templateStart
    stringem = str(data1["first"])
    utso = str(data1["last"])
    name = data1["name"]
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
    <div class="col"><canvas id="canvas" width="600" height="500"></canvas></div>"""

    for id, mess in myMessages.items():
        content += '<div class="col blue">'
        print(mess)
        content += '<a href="#" class="text-light bg-dark"> ' + str(id) + " : </a>"
        content += mess
        content += '<div>'


    #exit()

    content += """"
  </div>
</div>
"""
    print(values)
    allMessages =  values["all"]
    print(allMessages)
    content += getScript(keys, allMessages, values[person1], values[person2], person1, person2)
    return content


def processWord(words, toProcess):
    print(words)
    wordUnits = toProcess.split(" ")
    wordUnits = map(lambda x: x.lower(), wordUnits)
    words.extend(wordUnits)
    print(wordUnits)
    ##print(words)
    return sorted(set(words))


def processJson(file):
    print(file)
    dateStat = {}
    person1Stat = {}
    person2Stat = {}
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
        person1 = encodeText(person1)

        person2 = names[1]["name"]
        person2 = encodeText(person2)

        messages = data['messages']
        firstMess = messages[len(messages)-1]['timestamp_ms']
        lastMess = messages[0]['timestamp_ms']
        mess_count = len(messages)
        htmlFilename = str(mess_count) + " " + encodeText(person1) + "-" + encodeText(person2) + " " + getDate(firstMess).split()[0] + "---" + \
                       getDate(lastMess).split()[0]  +".html"
        htmlFilename = htmlFilename.replace(" ", "_")
        print(htmlFilename)
        if (os.path.exists(htmlFilename)):
            return 0
        print(person1)
        print(person2)
        print("végeee")
        #exit()
         #print(messages)
        print("DArab üzenet " + str(mess_count))
        print(messages[0])
        timeDiff = lastMess - firstMess
        csabauzik = 0
        counter = 0
        myMessages = {}
        words = []
        for message in messages:
            print("\n")
            name = encodeText(message['sender_name'])
            if "content" in message:
                data = message['content']
                print(encodeText(data))

                # https://stackoverflow.com/questions/26614323/in-what-world-would-u00c3-u00a9-become-%C3%A9
            if ((name == person2) & ("content" in message)):
                print(data)
                #exit()
                print(counter)
                csabauzik = csabauzik + 1
                date = getDate(message['timestamp_ms'])
                print(encodeText(person2) + " [" + date + "] : ")
                dateStat = processDateStat(dateStat, date)
                person2Stat = processDateStat(person2Stat, date)
                datam = message['content']
                #print(encodeText(datam))

                toProcess = encodeText(datam)
                #
                words = processWord(words, toProcess)
                message = encodeText(person2 + " " + date + " : \n " + datam)
                myMessages[counter] = message

            print(person1)
            print(name)
            print("faszom")
           #exit()
            if ((name == person1) & ("content" in message)):
                print(person1)
                print("BEAA")
                print(data)
                #exit()
                print(data)
                print(name)
                print("szar p1")
                #exit()
                print(counter)
                date = getDate(message['timestamp_ms'])
                print(encodeText(person1 ) + " " + date + " : ")
                dateStat = processDateStat(dateStat, date)
                person1Stat = processDateStat(person1Stat, date)
                datam = message['content']
                #print(encodeText(datam))
                toProcess = encodeText(datam)
                #
                words = processWord(words, toProcess)
                message = encodeText(person1 + " " + date + " : \n " + datam)
                myMessages[counter] = message
                print("==========")
                print(message)
                print("__")
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
        person1Stat = list(person1Stat.values())[::-1]
        person2Stat = list(person2Stat.values())[::-1]
        print(dateStat)
        exit()
        values = {}
        values["all"] = dateStatKValues

        #exit()
        values[person1] = person1Stat
        values[person2] = person2Stat

        print(htmlFilename)


        data = {}
        data["person1"] = person1
        data["person2"] = person2
        data["words"] = words
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

        content = generateContent(dateStatList, values, data)

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
        print("itt")
        exit()
counter = 0

fileCounter = 0
for file in onlyDirs:
    path =mypath2 + file + "\message_1.json"
    path2 =mypath2 + file + "\message_2.json"
    path3 =mypath2 + file + "\message_3.json"
    path4 =mypath2 + file + "\message_4.json"
    path5 =mypath2 + file + "\message_5.json"


    with open(path) as json_file:
        print(counter)
        counter += 1
        #print(json_file)
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
    if fileCounter >= 2:
        exit()
    if (os._exists(path2)):
        fileCounter += processJson(path2)
