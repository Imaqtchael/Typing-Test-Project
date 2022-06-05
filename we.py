import PyQt5
from matplotlib import pyplot as plt
import numpy as np
from tinydb import TinyDB, Query
from PyQt5 import QtGui

User = Query()
player = 'Justin'
mode = 'random'

plt.ion()

plt.rcParams['axes.facecolor'] = '#323437'
plt.rcParams['axes.edgecolor'] = '#646669'
plt.rcParams['xtick.color'] = '#D1D0C5'
plt.rcParams['ytick.color'] = '#D1D0C5'
plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.facecolor'] = '#323437'

class History():
    def __init__(self):
        super(History, self).__init__()
        self.accuDB = TinyDB('files/{}/accuracy/accuracy.json'.format(mode))
        self.wpmDB = TinyDB('files/{}/wpm/wpm.json'.format(mode))
        self.accuList, self.wpmList = None, None
        self.accu, self.wpm = None, None
        self.fig = None

    def show(self):
        self.accuList = self.accuDB.search(User.name == player)[0]['accuracyList']
        self.wpmList = self.wpmDB.search(User.name == player)[0]['wpmList']
        
        print(self.accuList)
        print(self.wpmList)

        accu = self.accuDB.search(User.name == player)[0]['accuracy']
        wpm = self.wpmDB.search(User.name == player)[0]['wpm']

        font1 = {'family': 'Roboto Mono', 'color': 'red', 'size': 10}
        font2 = {'family': 'Roboto Mono', 'color': '#E2B714', 'size': 10}
        font3 = {'family': 'Roboto Mono', 'color': '#D1D0C5', 'size': 10}

        Aypoints = np.array(self.accuList)
        Wypoints = np.array(self.wpmList)

        
        #plt.rcParams['figure.figsize'] = (7.5, 6)

        self.fig, self.ax = plt.subplots(2, 1, sharex=True)

        self.fig.text(0.20, 0.95, "average wpm: ", ha="center", va="bottom", fontdict=font3)
        self.fig.text(0.30, 0.95, "{}".format(int(wpm)), ha="center", va="bottom", fontdict=font1)
        self.fig.text(0.65,0.95,"average accuracy: ", ha="center", va="bottom", fontdict=font3)
        self.fig.text(0.77,0.95,"{}".format(int(accu)), ha="center", va="bottom", fontdict=font2)
        self.fig.text(0.795,0.95,"%", ha="center", va="bottom", fontdict=font1)

        self.wpm, = self.ax[0].plot(Wypoints, color='r')
        #self.ax[0].plot(Wypoints, color='r')
        #ax[0].set_xlim(xmin=1)
        self.ax[0].grid()
        #ax[0].set_xlabel("Number of Tests", fontdict=font3)
        self.ax[0].set_ylabel("Words per minute", fontdict=font1)

        self.accu, = self.ax[1].plot(Aypoints, color='#E2B714')
        #self.ax[1].plot(Aypoints, color='#E2B714')
        #ax[1].set_xlim(xmin=1)
        self.ax[1].grid()
        self.ax[1].set_xlabel("Number of Tests", fontdict=font3)
        self.ax[1].set_ylabel("Accuracy", fontdict=font2)

       
        win = self.fig.canvas.window()
        win.setFixedHeight(win.height())
        win.setMinimumWidth(win.width())
        win.setWindowTitle("History Data: [{}]".format(mode.capitalize()))
        win.setWindowIcon(QtGui.QIcon("files/pictures/icon.png"))
        

        plt.subplots_adjust(left=0.1,
                            bottom=0.1, 
                            right=0.9, 
                            top=0.9, 
                            wspace=0.4, 
                            hspace=0.4)

        print("Done showing...")
        
    def update(self):
        self.accuDB = TinyDB('files/{}/accuracy/accuracy.json'.format(mode))
        self.wpmDB = TinyDB('files/{}/wpm/wpm.json'.format(mode))

        self.accuList = self.accuDB.search(User.name == player)[0]['accuracyList']
        self.wpmList = self.wpmDB.search(User.name == player)[0]['wpmList']
        
        print(self.accuList)
        print(self.wpmList)

        accu = self.accuDB.search(User.name == player)[0]['accuracy']
        wpm = self.wpmDB.search(User.name == player)[0]['wpm']

        Aypoints = np.array(self.accuList)
        Wypoints = np.array(self.wpmList)

        print(Aypoints)
        print(Wypoints)

        '''self.accu.set_xdata(Aypoints)
        self.accu.set_ydata(np.array(range(len(Aypoints))))
        
        self.wpm.set_xdata(Wypoints)
        self.wpm.set_ydata(np.array(range(len(Wypoints))))'''

        self.wpm, = self.ax[0].plot(Wypoints, color='r')
        self.accu, = self.ax[1].plot(Aypoints, color='#E2B714')

        
        #self.fig.canvas.flush_events()
        print("Done updating...")

history = History()
history.show()
input("Before update\n")
for i in range(10):
    history.update()

    

    input("Press any key: ")
