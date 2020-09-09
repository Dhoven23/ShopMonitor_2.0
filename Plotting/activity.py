import matplotlib.pyplot as plt
from Data.day import Day
import numpy as np
from Data.mongo_setup import global_init,global_disconnect

global_init('DHoven','12345')

def plotins():
    X = []
    labels = []
    t = []
    n = 0
    for day in Day.objects:
        n += 1
        t.append(n)
        print(day.date)
        X.append(day.logs)
        labels.append(day.date[5:10])
    plt.bar(t, X)
    plt.title('Daily users')
    plt.xticks(t, labels, rotation=45)
    plt.ylabel('Students')
    plt.show()



