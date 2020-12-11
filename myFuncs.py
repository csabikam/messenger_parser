import os
import random
import re
from os.path import isfile, join
import json
import ftfy
from datetime import datetime
import numpy as np
import nltk
import io




def getDateOfNow() -> str:
    dt_obj = datetime.now()
    result = str(dt_obj).split(" ")[0]
    return result


now = datetime.now()
print(now)
print(type(now))
getDateResult = getDateOfNow()
print("getDate result : " + getDateResult)