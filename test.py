import datetime
import mongoengine
import Data.mongo_setup as mongo 
from Data.day import Day

mongo.global_init('DHoven','12345')

def find_day(date: str) -> Day:
    day0 = Day.objects(date=date).first()

    return day0

date_time_str = '2021-01-03'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
today = datetime.date.today()

delta = date_time_obj.date() - today
delta = delta.days
print(delta)
delta = int(delta)

date_list = [today - datetime.timedelta(days=x) for x in range(-delta)]
#print('Date:', date_time_obj.date())
#print('Today:', str(today))
#print(delta)

for date in date_list:
    day0 = find_day(date)
    print(day0.logs)

mongo.global_disconnect()