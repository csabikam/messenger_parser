from bs4 import BeautifulSoup
import sys
import re
import os
import json
import time
from datetime import datetime, timezone

# import urllib2

msnOutput="msnOutput.html";
print('This message will be displayed on the screen.')
if os.path.exists(msnOutput):
  os.remove(msnOutput)
else:
  print("The file does not exist : ", msnOutput)

url = "anita.html"
page = open(url, "r", encoding="utf-8")
soup = BeautifulSoup(page.read(), "html.parser")

original_stdout = sys.stdout # Save a reference to the original standard output

htmlStart="""<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>

<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Your analysis with X (todo)</a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">Link <span class="sr-only">(current)</span></a></li>
        <li><a href="#">Stats</a></li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="#">Separated link</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="#">One more separated link</a></li>
          </ul>
        </li>
      </ul>
      <form class="navbar-form navbar-left">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="#dates">Dates</a></li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Dropdown <span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="#">Separated link</a></li>
          </ul>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>

<div class="container"><table class="table table-dark">
<tbody>

"""
htmlEnd='</div></body></html>'
listStartData="""<tr><td><div class="p-3 mb-2 bg-danger text-white">"""
listStart="""<tr><td><div class="p-3 mb-2 bg-info text-white">"""
listStartB="""<tr><td><div class="p-3 mb-2 bg-warning text-white">"""
listEnd="""</div></td></tr></tbody>
"""





messages = soup.find_all('div', {'class' : 'msg'})
#f.write("szar")

numberOfWords=0
listOfWords= []
wordsHash={}

startingDate = None
endingDate = None


def processText(param):
    words = param.split()
    countWord=len(words)
    global numberOfWords
    global listOfWords
    global wordsHash
    numberOfWords=numberOfWords+countWord
    listOfWords.append(words)
    for i in words:
        if i in wordsHash:
            wordsHash[i] = wordsHash[i]+1
        else:
            wordsHash[i] = 1
    listOfWords
    pass


with open(msnOutput, 'a+', encoding="utf-8") as f:
    print(htmlStart, file=f)
    counter=0
    x = 800914507
    y = 1456410120
    for message in messages:
        #print(city)
        print("================counter : " ,  counter)
        tagsoup = BeautifulSoup(str(message), "html.parser")
        #print(tagsoup.prettify())
        tag = tagsoup.div.div['data-store']
        tagjson = json.loads(tag)
        timestamp = tagjson["timestamp"]
        thatTime = datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        thatDate = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
        thatDateYear = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y')
        thatDateMonth = datetime.utcfromtimestamp(timestamp / 1000).strftime('%m')
        thatDateDay = datetime.utcfromtimestamp(timestamp / 1000).strftime('%d')
        if startingDate == None:
            startingDate = datetime(int(thatDateYear), int(thatDateMonth), int(thatDateDay))
        actualDate = datetime(int(thatDateYear), int(thatDateMonth), int(thatDateDay))
        if endingDate == None:
            endingDate = actualDate
        if endingDate < actualDate:
            endingDate = actualDate
        author = tagjson["author"]
        name = ""
        if ( author == x):
            name = "X"
        else:
            name = "Csaba"
        print(name)
        print(timestamp)
        print(thatTime)
        print(author)
        if name == "X":
            print(listStart, file=f)
        else:
            print(listStartB, file=f)
        print('<h4>', file=f)
        print((counter), file=f)
        print("</h4>", file=f)
        print('<span class="', counter , ' align-middle">', file=f)
        print("</span>", file=f)
        print(name, ' : ', '<b>', "message.get_text()", '</b>', file=f)
        print('<h6>', thatTime, '</h6>', file=f)
        processText(message.get_text())
        counter=counter+1
        print(listEnd, file=f)

    res = []
    for i in listOfWords:
        if i not in res:
            res.append(i)
    timeDiff = endingDate - startingDate
    print(listStartData, file=f)
    print('<div id="dates">', file=f)
    print('<h4>', file=f)
    print("Starting date:", file=f)
    print(startingDate, file=f)
    print("</h4>", file=f)
    print('<h4>', file=f)
    print("Ending Date", file=f)
    print(endingDate, file=f)
    print("</h4>", file=f)
    print('<h3>', file=f)
    print("Total length", file=f)
    print(timeDiff, file=f)
    print("</h3>", file=f)
    print("</div>", file=f)
    print(listEnd, file=f)
    print("</table>", file=f)
    print("Number of words : " , len(res), file=f)
    print("Words : ", res, file=f)
    print('<p class="text-warning">', file=f)
    sorted(wordsHash.items(), key=lambda x: x[1], reverse=True)
    result = json.dumps(wordsHash, ensure_ascii=False)
    print(result, "</p>", file=f)
    print(listOfWords, file=f)
    print(htmlEnd, file=f)


print('End of imprinting.')


#print(soup.prettify())


