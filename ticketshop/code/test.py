import datetime

date = str(datetime.datetime.now())

date = date.rsplit(":", 1)
date = date[0]

print(date)