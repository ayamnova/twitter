import os
import os.path
import json
import re

organized = "crisis/crisis/2018"
unorganized = "crisis/crisis/2018/05"
pattern = re.compile(r'\s(\w{3})\s(\d{2})\s(\d{2})')


for e in os.listdir(unorganized):
    test = os.path.join(unorganized, e)
    if os.path.isfile(os.path.join(test)):
        time = ""
        try:
            f = open(test, 'r', encoding="utf8")
            time = json.loads(f.readline())
            f.close()
            time = time["created_at"]
        except:
            print("error")
        stuff = re.search(pattern, time)
        print(stuff)
        if stuff is not None:
            temp = ""
            month, day, hour = stuff.groups()
            if month == "May":
                month = "05"
            elif month == "Jun":
                month = "06"
            if month not in os.listdir(organized):
                temp = os.path.join(organized, month)
                os.mkdir(temp)
            temp = os.path.join(organized, month)
            if day not in os.listdir(temp):
                temp = os.path.join(temp, day)
                os.mkdir(temp)
                os.mkdir(os.path.join(temp, hour))
            temp = os.path.join(temp, day)
            if hour not in os.listdir(temp):
                os.mkdir(os.path.join(temp, hour))

            temp = os.path.join(temp, hour)
            if os.path.basename(test) not in os.listdir(temp): 
                os.rename(test, os.path.join(temp, os.path.basename(test)))
            else:
                print("skipping file {0}".format(os.path.basename(test)))
