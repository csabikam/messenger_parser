import random
import string
import sys

print(sys.getdefaultencoding())

result = ""


letter = """
Hát hellóbelló Dörikám ! 

Nyilván meglep , hogy még egy normális levelet sem tudsz kapni tőlem . 
Nem hogy nem vettem semmit , de még ez a szenvedés is . 
Hát mire jó ez ? Kérdhetnéd teljes joggal .
Valójában ezt magadnak köszönheted . 
Te vagy az , aki túl okos vagy . És egy ilyen okoska szenvedjen csak .
Bízom benned , úgyis kitalálod valahogy . 
Mondjuk lehet , hogy nem két perc lesz . De nézd a szép oldalát .
Írtam egy programot csak azért , hogy te szórakozhass ezzel Barcikán . 
Lehetett volna rosszabb is . Ha például 
különveszem a kis és nagy karaktereket . 
Dehát azért akkora rohadék nem vagyok .

Kezdődjön hát a karácsonyi levél tényleges része :
Dórikám ! Vagyis Okoskisasszony !
Szeretném ha tudnád , hogy csak úgy nem szórakozok ilyen faszságokkal . 
A tény, hogy nekiálltam téged megszopatni ( igen , tudom nem abban az értelemben , ahogy szereted ezt csinálni )
azt mutatja , hogy fontos vagy nekem és hogy nagyon hálás vagyok az Úr jézuskrisztusnak , hogy megteremtett 
téged édesanyád általa , és ideszülettéla földre , hogy segíts nekem megváltani a földet . Piciről picire .
Továbbá köszönöm neked , hogy ilyen remek jellem vagy , és hogy megbízható , diszkrét , okos és értelmes vagy . 
Hogy képes vagy belátni , ha hibázol , és lenyelni a békát , ha nekem van igazam . És igen , néha neked is van igazad . Néha !

Kívánom tehát hogy a jövő év is sok spontán és boldog és katartikus pillanatban , beszélgetésben gazdag legyen .
Már ha valaha megfejted ezt a szaros levelet . Biztos ezerszer megbántad , hogy programozó vagyok . 
Úgy kell neked , minek barátkozol hülyékkel . Tehát legyen szép karácsonyod , jó fejtegetést , és kapj sok ajándékot .

Várom a jövő évet , mit hoz , vagyis hozok a vízöntő korába . Majd én teleöntöm tiszta vízzel . És te lehetsz a krampusz , aki segít .
Aki nem segít , annak le lesz csippentve kisollóval a csiklója . Aucs . Ugye ezt te sem akarod .

Szép karácsonyt  Okoska !

üdv: 
Csabinnyó

ui : igen tudom ezért a golyóimon állsz bosszút te golyóroppantó
"""
letters = []
greek = [
    '\u0393',
    '\u0394',
    '\u0398',
    '\u039B',
    '\u039E',
    '\u03A0',
    '\u03A3',
    '\u03A6',
    '\u03A7',
    '\u03A8',
    '\u03A9',
    '\u03b2',
    '\u03e2',
    '\u03e8',
    '\u03ea',
    '\u03ec',
    '\u0416',
    '\u0414',
    '\u0417',
    '\u0418',
    '\u042f',
    '\u0460',
    '\u0489',
    '\u04c3',
    '\u07dc',
    '\u07db',
    '\u07f7',
    '\u0965',
    '\u0b6a',
    '+',
    '-',
    '%',
    'Ö',
    '=',
    '@',
    '#',
    '&',
    '<',
    '>',
    '€',
    '$'


]

print(greek)
#exit()


def getDict(letters, greek):
    random.shuffle(letters)
    random.shuffle(greek)
    # print(letters)
    # print(greek)
    # print("letters len  " + str(len(letters)))
    # print("greek len  " + str(len(greek)))
    dict = {}
    for x in range(0,len(letters)):
        # print(x)
        dict[letters[x]] = greek[x]
    return dict


for x in range(0, len(letter)):
    print(letter[x])
    letters.append((letter[x]).capitalize())

print(set(letters))
letters = set(letters)
letters = list(letters)
print(len(letters))
greek = set(greek)
greek = list(greek)
print(greek)
print(len(greek))







def encodeLetter(dict, letter):
    dict[" "] = "   "
    dict["\n"] = "\n\n"
    result = ""
    for x in letter:
        result += dict[x.capitalize()]
    letter.replace(dict[" "], " ")
    return result


def printHelpingLetters(dict, helpingChars):
    for x in helpingChars:
        print(x + "      =          " + dict[x])

d = getDict(letters, greek)

encodedLetter = encodeLetter(d, letter)
helpingChars = [".", ",", "!", "(", ")", ":", "?"]
# print(encodedLetter)
#
# print("letter : " + letter)
# print("letter len " + str(len(letter)))
# print("enc letter len " + str(len(encodedLetter)))
print("enc letter : " + encodedLetter)
printHelpingLetters(d, helpingChars)
print("======")

for i in d:
    print(i + " = " )






