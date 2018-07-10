import json
import re
f_in = "./Syria_25_5"
pattern = re.compile(r'\s(\w{3})\s(\d{2})\s(\d{2})')

f_26 = "./crisis/crisis/2018/06/26/flume"
f_28 = "./crisis/crisis/2018/06/28/flume"
f_29 = "./crisis/crisis/2018/06/29/flume"
f_30 = "./crisis/crisis/2018/06/30/flume"
f_01 = "./crisis/crisis/2018/07/01/flume"

f26 = open(f_26, 'w')
f28 = open(f_28, 'w')
f29 = open(f_29, 'w')
f30 = open(f_30, 'w')
f01 = open(f_01, 'w')


f = open(f_in, 'r')
tweets = dict()

for line in f:
    try:
        tw = json.loads(line)
        time = tw['created_at']
        stuff = re.search(pattern, time)
        if stuff is not None:
            temp = ""
            month, day, hour = stuff.groups()
            print(day)
            if day not in tweets:
                tweets[day] = [tw]
            else:
                tweets[day] += [tw]
    except:
        continue

for t in tweets["26"]:
    json.dump(t, f26)
    f26.write("\n")
for t in tweets["28"]:
    json.dump(t, f28)
    f28.write("\n")
for t in tweets["29"]:
    json.dump(t, f29)
    f29.write("\n")
for t in tweets["30"]:
    json.dump(t, f30)
    f30.write("\n")
for t in tweets["01"]:
    json.dump(t, f01)
    f01.write("\n")
