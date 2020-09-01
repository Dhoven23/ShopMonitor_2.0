import datetime

date_time_str = '2020-06-29'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
today = datetime.date.today()

delta = date_time_obj.date() - today

print('Date:', date_time_obj.date())
print('Today:', str(today))
print(delta)
