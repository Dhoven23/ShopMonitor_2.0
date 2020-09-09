import matplotlib.pyplot as plt
from Data.day import Day
import numpy as np
from Data.mongo_setup import global_init,global_disconnect

global_init('DHoven','12345')

def plotins():
    X = []
    Y = []
    labels = []
    t = []
    t1=[]
    t2 = []
    n = 0
    for day in Day.objects:
        n += 1
        t.append(n)
        t1.append(n-0.25)
        t2.append(n+0.25)
        print(day.date)
        X.append(day.logs)
        Y.append(day.capstone_logs)
        labels.append(day.date[5:10])
    ax = plt.subplot(111)

    normal = ax.bar(t, X, width=0.5, label = 'normal')

    capstone = ax.bar(t2, Y, width=0.5, label = 'Capstone')
    plt.title('Daily users')
    plt.xticks(t, labels, rotation=45)
    plt.legend(handles = [capstone, normal])
    plt.ylabel('Students')
    plt.show()



