import matplotlib.pyplot as plt
from Data.day import Day


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

        t1.append(n-0.2)
        t2.append(n+0.2)

        X.append(day.logs)
        Y.append(day.capstone_logs)
        labels.append(day.date[5:10])
    ax = plt.subplot()
    M = 30
    t1 = t1[-M:]
    t2 = t2[-M:]
    X = X[-M:]
    Y = Y[-M:]
    t = t[-M:]
    normal = ax.bar(t1, X, width=0.4, label = 'normal',color='blue')

    capstone = ax.bar(t2, Y, width=0.4, label = 'Capstone',color='orange')
    fig = plt.gcf()
    fig.set_size_inches(8,6)
    plt.title('Daily users',fontsize=20)
    plt.xticks(t, labels, rotation=45)
    plt.legend(handles = [capstone, normal])
    plt.ylabel('Students')
    plt.show()



