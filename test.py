import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from tinydb import TinyDB, Query
from PyQt5 import QtGui

'''from tinydb import TinyDB

name = "accuracy"
db = TinyDB("files/{0}/{0}.json".format(name))

db.truncate()
db.insert({'name': 'Justin', name: 0, name + "List": []})
db.insert({'name': 'Barcenas', name: 0, name + "List": []})
db.insert({'name': 'Janessa', name: 0, name + "List": []})
db.insert({'name': 'Justine', name: 0, name + "List": []})'''

'''from bs4 import BeautifulSoup
from PyQt5 import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys, random, datetime, requests
from screeninfo import get_monitors
from tinydb import TinyDB, Query

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("try")
        self.setFixedSize(300, 300)
        self.initUI()

    def initUI(self):
        self.widget = QtWidgets.QTextEdit(self)
        self.widget.setAlignment(Qt.Qt.AlignCenter)
        self.widget.insertPlainText("hahahahhah")
        self.widget.setFixedSize(300, 300)

app = QApplication(sys.argv)
win = Window()
#win = WindowPick()
#win = Window("paragraph")
win.show()
sys.exit(app.exec_())'''

def tiny(sub):
    name = "accuracy"
    mode = 'random'
    

    def resetAcc():
        db = TinyDB("files/{0}/{0}.json".format('account'))
        db.truncate()
    
    def resetAW():
        db = TinyDB("files/{1}/{0}/{0}.json".format(name, mode))
        db.truncate()
        '''db.insert({'name': 'Justin', name: 0, name + "List": []})
        db.insert({'name': 'Barcenas', name: 0, name + "List": []})
        db.insert({'name': 'Janessa', name: 0, name + "List": []})
        db.insert({'name': 'Justine', name: 0, name + "List": []})'''

    if sub == 'acc':
        resetAcc()
    elif sub == 'aw':
        resetAW()


        
def matplot():


    User = Query()
    player = "J"

    accuDB = TinyDB('files/accuracy/accuracy.json')
    wpmDB = TinyDB('files/wpm/wpm.json')

    accuList = accuDB.search(User.name == player)[0]['accuracyList']
    wpmList = wpmDB.search(User.name == player)[0]['wpmList']

    font1 = {'family': 'Roboto Mono', 'color': 'red', 'size': 10}
    font2 = {'family': 'Roboto Mono', 'color': '#E2B714', 'size': 10}
    font3 = {'family': 'Roboto Mono', 'color': '#D1D0C5', 'size': 10}


    Aypoints = np.array(accuList)
    Wypoints = np.array(wpmList)

    plt.rcParams['axes.facecolor'] = '#323437'
    plt.rcParams['axes.edgecolor'] = '#646669'
    plt.rcParams['xtick.color'] = '#D1D0C5'
    plt.rcParams['ytick.color'] = '#D1D0C5'
    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['figure.facecolor'] = '#323437'
    plt.rcParams['figure.figsize'] = (7.5, 6)
    
    fig, ax = plt.subplots(2, 1)

    ax[0].grid()
    ax[0].set_xlabel("Number of Tests", fontdict=font3)
    ax[0].set_ylabel("Words per minute", fontdict=font1)

    ax[1].plot(Aypoints, color='#E2B714')
    ax[1].set_xlim(xmin=1)
    ax[1].grid()
    ax[1].set_xlabel("Number of Tests", fontdict=font3)
    ax[1].set_ylabel("Accuracy", fontdict=font2)

    print(type(fig))
    print(type(ax))
    win = fig.canvas.window()
    win.setFixedSize(win.size())
    win.setWindowTitle(" ")
    win.setWindowIcon(QtGui.QIcon("files/pictures/icon.png"))

    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

    plt.show()

    #data is being duplicated


'''matplotlib.use('TkAgg')
mng = plt.get_current_fig_manager()
mng.window.resizable(False, False)'''




'''plt.subplot(2, 1, 1)
plt.plot(Wypoints, c='r')
plt.grid()

plt.xlabel("Number of Tests", fontdict=font3)
plt.ylabel("Words per minute", fontdict=font1)

plt.subplot(2, 1, 2)
plt.plot(Aypoints, c='#E2B714')
plt.grid()

plt.xlabel("Number of Tests", fontdict=font3)
plt.ylabel("Accuracy", fontdict=font2)


plt.suptitle("History Graph", color='#D1D0C5')

plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)'''



#ax[0].set_xlim(xmin=1)


#plt.suptitle("History", color='#D1D0C5')

tiny('aw')