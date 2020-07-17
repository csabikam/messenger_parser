from bs4 import BeautifulSoup
import sys
import re
import os
import json
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

<div class="container"><table class="table table-dark">
<tbody>

"""
htmlEnd='</table></div></body></html>'
listStart="""<tr><td><div class="p-3 mb-2 bg-info text-white">"""
listEnd="""</div></td></tr></tbody>
"""





cities = soup.find_all('div', {'class' : 'msg'})
#f.write("szar")

numberOfWords=0
listOfWords= []
wordsHash={}


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
    for city in cities:
    #print(city)
        print(listStart, file=f)
        print('<h4>', file=f)
        print((counter), file=f)
        print("</h4>", file=f)
        print('<span id="',counter,'" class=align-middle">', file=f)
        print(city.get_text(), file=f)
        processText(city.get_text())
        print("</span>", file=f)
        print('<p class="text-info">', file=f)
        print("DATUM", file=f)
        print("</p>", file=f)
        counter=counter+1
        print(listEnd, file=f)
    print('<p class="text-info">', file=f)
    res = []
    for i in listOfWords:
        if i not in res:
            res.append(i)
    print("Number of words : " , len(res), file=f)
    print("Words : ", res, file=f)
    print("</p>", file=f)
    print('<p class="text-warning">', file=f)
    sorted(wordsHash.items(), key=lambda x: x[1], reverse=True)
    result = json.dumps(wordsHash, ensure_ascii=False)
    print(result, "</p>", file=f)
    print(listOfWords, "</p>", file=f)
    print(htmlEnd, file=f)
    print

print('End of imprinting.')


#print(soup.prettify())


