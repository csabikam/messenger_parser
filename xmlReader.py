import xmltodict, json

with open('xml\gida88.xml', 'r', encoding="utf-8") as myfile:
    obj = xmltodict.parse(myfile.read())
print(json.dumps(obj["Log"]["Message"]))
msgList = obj["Log"]["Message"]
print(type(obj))
print(len(msgList))
counter = 0
for msg in msgList:
    print()
    print(counter)
    counter += 1
    #print(msg)
    dateAndTime = msg["@Date"] + " " + msg["@Time"]
    name = msg['From']['User']['@FriendlyName']
    if "#text" in msg['Text']:
        text = msg['Text']['#text']
    else:
        text = msg['Text']
    print(dateAndTime + " " + name + ": " + text )
    print()
    pass
