from datetime import datetime, timedelta

now = datetime.now().date()
tommorow = timedelta(days=+10)
daynew = now + tommorow
print(daynew)