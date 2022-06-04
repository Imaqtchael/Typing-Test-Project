from turtle import width
from bs4 import BeautifulSoup
from PyQt5 import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys, random, datetime, requests
from screeninfo import get_monitors
from tinydb import TinyDB, Query

HEIGHT, WIDTH = int(get_monitors()[0].height / 2), int(get_monitors()[0].width / 2)
#HEIGHT, WIDTH = int(HEIGHT * 1.7), int(WIDTH * 1.7)
fontWeight = int(15 * 1.7)
print(HEIGHT)
print(WIDTH)

db = TinyDB('files/account/account.json')
User = Query()

db.truncate()
db.insert({'name': 'Justin', 'pass': 'atheist'})
db.insert({'name': 'Barcenas', 'pass': 'atheista'})
db.insert({'name': 'Janessa', 'pass': 'maganda'})
db.insert({'name': 'Justine', 'pass': "janessa"})

player = ""
class LogIn(QWidget):
    def __init__(self):
        super(LogIn, self).__init__()
        self.setFixedSize(300, 130)
        self.setWindowTitle("Login")
        self.initUI()
        self.results = []
        self.password = ""
        

    def initUI(self):
        self.grandLayout = QtWidgets.QVBoxLayout(self)
        self.nameHlayout = QtWidgets.QHBoxLayout()
        self.passHlayout = QtWidgets.QHBoxLayout()
        self.buttonHlayout = QtWidgets.QHBoxLayout()

        self.nameLabel = QtWidgets.QLabel(self)
        self.nameLabel.setText("Username: ")
        self.nameLabel.setFont(QtGui.QFont("Roboto Mono", 15))

        self.nameTextEdit = QtWidgets.QTextEdit(self)
        self.nameTextEdit.setFont(QtGui.QFont("Roboto Mono", 15))
        self.nameTextEdit.setMaximumHeight(30)
        self.nameTextEdit.setObjectName("UserTE")
        self.nameTextEdit.textChanged.connect(self.checkUser)
        self.nameTextEdit.setTabChangesFocus(True)
        self.nameTextEdit.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        #self.nameTextEdit.installEventFilter(self)

        self.nameCursor = QtGui.QTextCursor(self.nameTextEdit.textCursor())

        self.passLabel = QtWidgets.QLabel(self)
        self.passLabel.setText("Password:  ")
        self.passLabel.setFont(QtGui.QFont("Roboto Mono", 15))
        
        self.passTextEdit = QtWidgets.QTextEdit(self)
        self.passTextEdit.setFont(QtGui.QFont("Roboto Mono", 15))
        self.passTextEdit.setMaximumHeight(30)
        self.passTextEdit.setObjectName("PassTE")
        self.passTextEdit.textChanged.connect(self.checkPass)
        self.passTextEdit.setTabChangesFocus(True)
        self.passTextEdit.installEventFilter(self)
        self.passTextEdit.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

        self.passCursor = QtGui.QTextCursor(self.passTextEdit.textCursor())

        self.loginButton = QtWidgets.QPushButton(self)
        self.loginButton.setText("Login")
        self.loginButton.setFont(QtGui.QFont("Roboto Mono", 15))
        self.loginButton.clicked.connect(self.login)
        self.loginButton.setObjectName("login")

        self.createButton = QtWidgets.QPushButton(self)
        self.createButton.setText("Create")
        self.createButton.setFont(QtGui.QFont("Roboto Mono", 15))
        self.createButton.clicked.connect(self.createUser)
        self.createButton.setObjectName("create")

        self.nameHlayout.addWidget(self.nameLabel)
        self.nameHlayout.addWidget(self.nameTextEdit)

        self.passHlayout.addWidget(self.passLabel)
        self.passHlayout.addWidget(self.passTextEdit)

        self.buttonHlayout.addWidget(self.createButton)
        self.buttonHlayout.addWidget(self.loginButton)

        self.grandLayout.addLayout(self.nameHlayout)
        self.grandLayout.addLayout(self.passHlayout)
        self.grandLayout.addLayout(self.buttonHlayout)

    def createUser(self):
        userName = self.nameTextEdit.toPlainText()
        passWord = self.passTextEdit.toPlainText()
        if len(db.search(User.name == userName)) == 0:
            db.insert({'name': userName, 'pass': passWord})
            accuDB = TinyDB("files/accuracy/accuracy.json")
            accuDB.insert({'name': userName, 'accuracy': 0, 'accuracyList': []})
            wpmDB = TinyDB("files/wpm/wpm.json")
            wpmDB.insert({'name': userName, 'wpm': 0, 'wpmList': []})
            
            self.nameTextEdit.setText("")
            self.passTextEdit.setText("")
            
            #self.passTextEdit.moveCursor(QtGui.QTextCursor.End)
            #self.passCursor = QtGui.QTextCursor(self.passTextEdit.document().findBlockByLineNumber(0))
            #self.passTextEdit.setTextCursor(self.passCursor)
            #print(self.passTextEdit.toPlainText())
            self.nameTextEdit.setFocus()
        print(db.all())

    def login(self):
        userName = self.nameTextEdit.toPlainText()
        passWord = self.password
        if self.results[0]['name'] == userName and passWord == self.results[0]['pass']:
            global player
            player = userName
            self.nameTextEdit.setText("")
            self.passTextEdit.setText("")
            self.nameTextEdit.setFocus()
            self.win = WindowPick()
            self.win.show()

    def checkUser(self):
        self.nameTextEdit.blockSignals(True)
        userName = self.nameTextEdit.toPlainText()
        textLength = len(userName)
        self.results = db.search(User.name == userName)
        
        if textLength > 8:
            print(8)
            userName = userName[:8]
            if len(self.results) == 1:
                self.nameTextEdit.setText("<font color='#D1D0C5'>{}</font>".format(userName))
                print("ha")
            elif len(self.results) == 0:
                self.nameTextEdit.setText("<font color='red'><u>{}</u></font>".format(userName))
                print("he")
        elif len(self.results) == 0:
            self.nameTextEdit.setText("<font color='red'><u>{}</u></font>".format(userName))
            print("hi")
        elif len(self.results) == 1:
            self.nameTextEdit.setText("<font color='#D1D0C5'>{}</font>".format(userName))
            print("ho")
        textLength = len(userName)
        print("{} {} {}".format(userName, textLength, self.results))
        self.nameTextEdit.blockSignals(False)
        self.nameTextEdit.moveCursor(QtGui.QTextCursor.End)
        #self.nameCursor.setPosition(textLength)
        #self.nameTextEdit.setTextCursor(self.nameCursor)
        '''self.nameTextEdit.blockSignals(True)
        userName = self.nameTextEdit.toPlainText()
        print(userName)

        if userName != "admin":
            self.nameTextEdit.setText("<font color='red'><u>{}</u></font>".format(userName))
        else:
            self.nameTextEdit.setText("<font color='#D1D0C5'>{}</font>".format(userName))
        self.nameTextEdit.blockSignals(False)
        textLength = len(self.nameTextEdit.toPlainText())
        self.nameCursor.setPosition(textLength)
        self.nameTextEdit.setTextCursor(self.nameCursor)'''

    def checkPass(self):
        self.passTextEdit.blockSignals(True)
        if len(self.results) == 0:
            print("len == 0")
            passwordText = self.passTextEdit.toPlainText()
            if len(passwordText) > 8:
                self.passTextEdit.setText(passwordText[:8])
                self.passTextEdit.moveCursor(QtGui.QTextCursor.End)
            self.passTextEdit.blockSignals(False)
            return
        passwordText = self.passTextEdit.toPlainText()
        #passwordText = passwordText.strip("\n")
        textLength = len(passwordText)
        try:
            self.password += passwordText[-1]
        except IndexError:
            self.password = ""

        if self.password != textLength:
            self.password = self.password[:textLength]
        password = self.results[0]['pass']
        '''try:
            password = self.results[0]['pass']
        except IndexError:
            return'''
        print(password + " here")
        #results = db.search(User.name == userName)
        mask = "*" * textLength
        if textLength > 8:
            passwordText = passwordText[:8]
            self.password = self.password[:8]
            textLength = len(passwordText)
            mask = "*" * textLength
            print("self.password: {}\npassword: {}".format(self.password, password))
            if self.password == password:
                self.passTextEdit.setText("<font color='#D1D0C5'>{}</font>".format(mask))
                print("ha")
            else:
                self.passTextEdit.setText("<font color='red'><u>{}</u></font>".format(mask))
                print("he")
        elif self.password != password:
            self.passTextEdit.setText("<font color='red'><u>{}</u></font>".format(mask))
            print("hi")
        elif self.password == password:
            self.passTextEdit.setText("<font color='#D1D0C5'>{}</font>".format(mask))
            print("ho")
        textLength = len(passwordText)
        print("{} {} {}".format(passwordText, textLength, self.results))
        self.passTextEdit.blockSignals(False)
        #self.passCursor.setPosition(textLength)
        #self.passTextEdit.setTextCursor(self.passCursor)
        self.passTextEdit.moveCursor(QtGui.QTextCursor.End)
        
        '''self.passTextEdit.blockSignals(True)
        passWord = self.passTextEdit.toPlainText()[-1]
        self.password += passWord
        print(self.password)
        if self.password != "admin":
            self.passTextEdit.setText("<font color='red'><u>{}</u></font>".format("*" * len(self.password)))
        else:
            self.passTextEdit.setText("<font color='#D1D0C5'>{}</font>".format("*" * len(self.password)))
        
        textLength = len(self.passTextEdit.toPlainText())
        if textLength == 8:
            self.passTextEdit.setReadOnly(True)
        self.passCursor.setPosition(textLength)
        self.passTextEdit.setTextCursor(self.passCursor)
        self.passTextEdit.blockSignals(False)
        print("checkPass() Done...")'''

    def eventFilter(self, obj, event):
        #print(self.passTextEdit.toPlainText())
        if event.type() == QtCore.QEvent.KeyPress and obj is self.passTextEdit:
            '''if not event.text().isalnum():
                return True'''
            if event.key() == QtCore.Qt.Key_Return:
                if self.passTextEdit.toPlainText() == "" or self.nameTextEdit.toPlainText() == "":
                    pass
                elif self.passTextEdit.toPlainText().isalnum():
                    self.createUser()
                elif len(self.results) == 1:
                    self.login()
                return True
        '''elif event.type() == QtCore.QEvent.KeyPress and obj is self.nameTextEdit:
            if event.key() == QtCore.Qt.Key_Return:
                return True'''
            
                    
        #print(self.passTextEdit.toPlainText())        
        return super().eventFilter(obj, event)
        '''if event.type() == QtCore.QEvent.KeyPress and (obj is self.passTextEdit or obj is self.nameTextEdit):
            if event.key() == QtCore.Qt.Key_Backspace and obj is self.passTextEdit:
                self.passTextEdit.blockSignals(True)
                print("check: {}".format(self.password))
                self.password = self.password[:-1]
                print("check2: {}".format(self.password))
                if self.password != "admin":
                    self.passTextEdit.setText("<font color='red'><u>{}</u></font>".format(self.password))
                else:
                    self.passTextEdit.setText("<font color='#D1D0C5'>{}</font>".format(self.password))
                #textLength = len(self.passTextEdit.toPlainText())
                #self.passCursor.setPosition(textLength)
                #self.passTextEdit.setTextCursor(self.passCursor)

                self.passTextEdit.setReadOnly(False)
                print(self.passTextEdit.toPlainText())
                print(self.password)
            elif event.key() == QtCore.Qt.Key_Return and self.password == "admin":
                self.passTextEdit.blockSignals(True)
                print("enter pressed")
            else:
                self.passTextEdit.blockSignals(False)
            
        return super().eventFilter(obj, event)'''
    
class WindowPick(QWidget):
    def __init__(self):
        super(WindowPick, self).__init__()
        self.setFixedSize(250, 80)
        self.setWindowTitle("Choose Mode")
        self.mode = ""
        self.initUI()

    def initUI(self):
        self.Hlayout = QtWidgets.QHBoxLayout(self)

        self.paragraphMode = QtWidgets.QPushButton(self)
        self.paragraphMode.setText("PARAGRAPH")
        self.paragraphMode.setFont(QtGui.QFont("Roboto Mono", 15))
        self.paragraphMode.clicked.connect(self.isParagraph)
        self.paragraphMode.setObjectName("chooseParagraph")

        self.randomWord = QtWidgets.QPushButton(self)
        self.randomWord.setText("RANDOM")
        self.randomWord.setFont(QtGui.QFont("Roboto Mono", 15))
        self.randomWord.clicked.connect(self.isRandom)
        self.randomWord.setObjectName("chooseRandom")

        self.Hlayout.addWidget(self.paragraphMode, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.Hlayout.addWidget(self.randomWord, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        
    def isRandom(self):
        self.win = RandomLen()
        self.win.show()
    
    def isParagraph(self):
        self.win = Window("paragraph")
        self.win.show()

class RandomLen(QWidget):
    def __init__(self):
        super(RandomLen, self).__init__() 
        self.setFixedSize(300, 58)
        self.setWindowTitle("Choose length")
        self.wordNum = ""
        self.num = 0
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QHBoxLayout(self)

        self.lenghtLabel = QtWidgets.QLabel(self)
        self.lenghtLabel.setText("Number of Words: ")
        self.lenghtLabel.setFont(QtGui.QFont("Roboto Mono", 15))

        self.length = QtWidgets.QLabel(self)
        self.length.setObjectName("length")
        self.length.setFont(QtGui.QFont("Roboto Mono", 15))

        self.layout.addWidget(self.lenghtLabel, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.length, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setObjectName("Length")

    def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_Backspace:
            self.wordNum = self.wordNum[:-1]
        elif event.key() == Qt.Qt.Key_Return:
            self.num = int(self.wordNum)
            self.win = Window("random", self.num)
            self.win.show()
        elif event.text().isnumeric():
            self.wordNum += event.text()
        self.length.setText(self.wordNum)

    def checkInput(self):
        pass
        '''isNum = self.length.toPlainText().isnumeric()
        print("ha")
        if (not isNum):
            if len(self.length.toPlainText()) == 1:
                print("nagtrue")
                self.length.clear()
            else:
                print("nagfalse")
                self.length.setText(self.length.toPlainText()[:-1])
                self.cursor = self.length.textCursor()
                self.cursor.setPosition(len(self.length.toPlainText()))
                self.length.setTextCursor(self.cursor)
        try:
            numWords = int(self.length.toPlainText())
            print(numWords)
        except ValueError:
            if len(self.length.toPlainText()) == 1:
                self.length.clear()
            else:
                self.length.setText(self.length.toPlainText()[:-1])'''

class Window(QMainWindow):
    def __init__(self, mode, num=None):
        super(Window, self).__init__()
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowTitle("Typing Test")
        self.setWindowIcon(QtGui.QIcon("files/pictures/icon.png"))
        self.mode = mode
        self.num = num
        self.startNew = False
        self.pressedBS = False
        self.correctInput = ""
        self.start = datetime.datetime.now()
        self.wrongInput = ""
        self.wrongChar = 0
        self.inputText = ""
        self.wordsPM = 0
        self.accuracy = 0
        self.initUI()
        self.newParagraph()
        print("Done superInit()")
        print(player)

    def initUI(self):
        #setting widgets: central is the biggest widget
        
        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)

        #central contains Vlayout which is the second biggest widget
        self.Vlayout = QtWidgets.QVBoxLayout(self.central)

        #right contains RVlyout, which then contains wpm, time, and accu
        self.right = QtWidgets.QWidget()
        self.right.setMinimumWidth(214)

        
        self.RVlayout = QtWidgets.QVBoxLayout(self.right)
        
        self.bigTopWidget = QtWidgets.QWidget()
        self.bigTopWidget.setMinimumHeight(120)


        #THlaytout contains text and right widget
        self.THlayout = QtWidgets.QHBoxLayout(self.bigTopWidget)
        self.THlayout.addWidget(self.right)
        self.THlayout.setObjectName("THlayout")

        #BVlayout contains the textedit and button
        self.BVlayout = QtWidgets.QVBoxLayout()
        self.BHlayout = QtWidgets.QHBoxLayout()
        
        #adding THlayout and BVlayout to Vlayout
        self.Vlayout.addWidget(self.bigTopWidget)
        self.Vlayout.addLayout(self.BVlayout)
        self.Vlayout.addLayout(self.BHlayout)

        

        self.wpm = QtWidgets.QLabel(self, wordWrap=True, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.wpm.setText("wpm: ")
        self.wpm.setFont(QtGui.QFont('Roboto Mono', 15))
        
        self.accu = QtWidgets.QLabel(self, wordWrap=True, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.accu.setText("accuracy: ")
        self.accu.setFont(QtGui.QFont('Roboto Mono', 15))
        
        self.elapsedTime = QtWidgets.QLabel(self, wordWrap=True, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.elapsedTime.setText("elapsed time: ")
        self.elapsedTime.setFont(QtGui.QFont('Roboto Mono', 15))

        self.profile = QtWidgets.QPushButton(self)
        self.profile.setText("View Profile")
        self.profile.setFont(QtGui.QFont('Roboto Mono', 12))
        self.profile.setObjectName('profile')

        #adding profile, wpm, accu, and time to RVlayout
        
        self.RVlayout.addWidget(self.accu)
        self.RVlayout.addWidget(self.wpm)
        self.RVlayout.addWidget(self.elapsedTime)
        
        self.RVlayout.addWidget(self.profile, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.textLabel = QtWidgets.QTextEdit(self)
        self.textLabel.setFont(QtGui.QFont('Roboto Mono', 20))
        self.textLabel.setMinimumWidth(900)
        self.textLabel.textChanged.connect(self.checkInput)
        self.textLabel.installEventFilter(self)
        self.textLabel.viewport().installEventFilter(self)
        self.textLabel.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

        self.textCursor = QtGui.QTextCursor(self.textLabel.textCursor())
        
        self.info = QtWidgets.QLabel(self, wordWrap=True, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignBottom)
        self.info.setText("press enter or space to start next test")
        self.info.setFont(QtGui.QFont('Roboto Mono', 12))
        self.info.setMinimumWidth(400)
        self.info.setHidden(True)

        self.BVlayout.addWidget(self.textLabel)
        #self.BVlayout.addSpacing(10)
        self.BVlayout.addWidget(self.info)

        #adding textspacer and right to THlayout
        #self.THlayout.addWidget(self.info)
        #self.THlayout.setSpacing(100)
        self.THlayout.addStretch()
        self.THlayout.addWidget(self.right)
      
        #nextbutton to have new paragraph
        self.nextButton = QtWidgets.QPushButton(self)
        self.nextButton.setObjectName("nextButton")
        self.nextButton.clicked.connect(self.newParagraph)
        self.nextButton.setFixedSize(50, 50)
        self.nextButton.setFocusPolicy(Qt.Qt.NoFocus)

        self.restartButton = QtWidgets.QPushButton(self)
        self.restartButton.setObjectName("restartButton")
        self.restartButton.clicked.connect(self.restart)
        self.restartButton.setFixedSize(50, 50)
        self.restartButton.setFocusPolicy(Qt.Qt.NoFocus)
        
        self.BHlayout.addWidget(self.nextButton, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.BHlayout.addWidget(self.restartButton, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        #adding button1 and input to BVlayout
        
        print("Done initUI()")

    def newParagraph(self):
        if self.mode == "paragraph":
            self.text = self.getParagraph()
        else: 
            self.text = self.load_words(self.num)
        self.textLabel.blockSignals(True)
        self.textLabel.setText("<p align='center'>{}</p>".format(self.text))
        self.textLabel.blockSignals(False)
        self.wrongInput = ""
        self.correctInput = ""
        self.inputText = ""
        self.wrongChar = 0

        #setting variable to checked later if the user started new paragraph
        self.startNew = True

        self.accu.setText("accuracy: ")
        self.wpm.setText("wpm: ")
        self.elapsedTime.setText("elapsed time: ")

        #removing input.isReadonly if the user goes to new paragraph
        self.textLabel.setReadOnly(False)
        print(self.text)
        self.nextButton.setFocusPolicy(Qt.Qt.NoFocus)
        self.info.setHidden(True)
        print("Done newParagraph()")

    def restart(self):
        self.wrongInput = ""
        self.correctInput = ""
        self.inputText = ""
        self.wrongChar = 0
        self.startNew = True
        self.textLabel.setReadOnly(False)
        self.textLabel.blockSignals(True)
        self.textLabel.setText("<p align='center'>{}</p>".format(self.text))
        self.textLabel.blockSignals(False)
        self.accu.setText("accuracy: <font color='#E2B714'>0</font><font color='red'>%</font>")
        self.wpm.setText("wpm: <font color='#E2B714'>0</font>")
        self.elapsedTime.setText("elapsed time: <font color='#E2B714'>0</font><font color='red'>s</font>")
        self.info.setHidden(True)
        print("Done restart()")


    def getParagraph(self):
        self.url = "https://randomword.com/paragraph"
        self.request = requests.get(self.url)
        self.doc = BeautifulSoup(self.request.text, "html.parser")
        self.tags = self.doc.find("div", {"id": "random_word_definition"}).string
        print("Done getParagraph()")
        return self.tags
 
    def load_words(self, num):
        with open('files/words_alpha.txt') as self.word_file:
            self.valid_wordsList = self.word_file.read().split()
            self.valid_words = []
            for i in range(num):
                randomWord = self.valid_wordsList[random.randrange(len(self.valid_wordsList))]
                self.valid_words.append(randomWord)
            self.paragraph = " ".join(self.valid_words)
        print()
        return self.paragraph

    def setTime(self):
        self.now = datetime.datetime.now()
        self.elapsed = self.now - self.start

        if int(self.elapsed.total_seconds()) > 60:
            self.mins = int(self.elapsed.total_seconds())//60
            self.secs = int(self.elapsed.total_seconds()) % 60
            self.elapsedText = "elapsed time: <font color='#E2B714'>{}</font><font color='red'>min/s</font> <font color='#E2B714'>{}</font><font color='red'>s</font>".format(self.mins, self.secs)
            self.elapsedTime.setText(self.elapsedText)
        else:
            self.secs = int(self.elapsed.total_seconds())
            self.elapsedText = "elapsed time: <font color='#E2B714'>{}</font><font color='red'>s</font>".format(self.secs)
            self.elapsedTime.setText(self.elapsedText)
        
        #print("Done setting time")

    def setWPM(self):
        self.elapsed = self.now - self.start
        if float(self.elapsed.total_seconds()) > 0:
            self.wordsPM = int((len(self.correctInput) / 4.7) * (60 / float(self.elapsed.total_seconds())))
            self.wpmText = "wpm: <font color='#E2B714'>{}</font>".format(self.wordsPM)
            self.wpm.setText(self.wpmText)

    def setAccu(self):
        try:
            self.accuracy = int(100 - ((self.wrongChar/len(self.correctInput)) * 100))
            self.accuText = "accuracy: <font color='#E2B714'>{}</font><font color='red'>%</font>".format(self.accuracy)
            self.accu.setText(self.accuText)
        except ZeroDivisionError:
            #print("have an error")
            pass
        
        #print("accu reset")

    '''def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_Return and self.inputText == "":
            self.newParagraph()
        else:
            if event.key() == Qt.Qt.Key_Backspace:
                self.inputText = self.inputText[:-1]
            elif not self.readOnly:
                self.inputText += event.text()
                print(len(self.inputText))

            elif event.key() == Qt.Qt.Key_Space or event.key() == Qt.Qt.Key_Return:
                self.newParagraph()
            print("typed: {}".format(self.inputText))
            print("he")
            self.checkInput()'''

    def eventFilter(self, obj, event):
        if obj is self.textLabel.viewport() and (event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick):
            print("mouse")
            if event.button() == QtCore.Qt.LeftButton:
                print("left")
                return True
            elif event.button() == QtCore.Qt.RightButton:
                print("right")
                return True
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textLabel:
            if event.key() == Qt.Qt.Key_Return and self.inputText == "":
                self.newParagraph()
                return True
            elif (event.key() == Qt.Qt.Key_Return or event.key() == Qt.Qt.Key_Space) and self.text == self.inputText:
                self.newParagraph()
                return True
            elif event.key() == Qt.Qt.Key_Return:
                return True
            elif event.key() == Qt.Qt.Key_Backspace and self.inputText == "":
                print('zero ' + self.inputText)
                return True
            elif event.key() == Qt.Qt.Key_Backspace:
                self.inputText = self.inputText[:-1]
                self.pressedBS = True
                print("backspace: " + self.inputText)
            

        return super().eventFilter(obj, event)

    def checkInputed(self):
        self.textLabel.blockSignals(True)
        
        self.textLabel.blockSignals(False)
        print(self.inputText)

    def checkInput(self):
        self.textLabel.blockSignals(True)
        if self.pressedBS == False:
            cursorPos = self.textLabel.textCursor().position()
            print("cursor is at: " + str(cursorPos))
            self.inputText += self.textLabel.toPlainText()[cursorPos - 1]
        else: 
            self.pressedBS = False
        self.inputContent = self.inputText
        print("input: " + self.inputContent)

        if len(self.inputContent) == 0:
            self.wrongInput = ""
            self.correctInput = ""
            self.textLabel.setText("<p align='center'>{}</p>".format(self.text))
            print("length is 0")

        if len(self.inputContent) > 0:
            print("length is greater than 0")
            if self.startNew:
                self.start = datetime.datetime.now()
                self.startNew = False
            self.setTime()
            if self.inputContent != self.text[:len(self.inputContent)]:
                print("text and input not equal")
                self.firstlen = len(self.wrongInput)
                self.wrongInput = self.text[len(self.correctInput):len(self.inputContent)]
                self.secondlen = len(self.wrongInput)
                if not (self.firstlen > self.secondlen): #adding to wrongChar if user is wrong and not backspacing
                    self.wrongChar += 1
                    print("wrongchar: " + str(self.wrongChar))
                self.textLabel.setText("<p align='center'><font color='#D1D0C5'>{}</font><font color='red'><u>{}</u></font>{}</p>".format(self.correctInput, self.wrongInput, self.text[len(self.correctInput)+len(self.wrongInput):]))
                self.textCursor.setPosition(len(self.correctInput) + len(self.wrongInput))
                self.textLabel.setTextCursor(self.textCursor)
  
            else:
                if len(self.inputContent) > len(self.correctInput):
                    self.correctInput += self.inputContent[-1]
                elif len(self.inputContent) < len(self.correctInput):
                    self.correctInput = self.inputContent
                else:
                    self.wrongInput = ""
                self.textLabel.setText("<p align='center'><font color='#D1D0C5'>{}</font>{}</p>".format(self.correctInput, self.text[len(self.correctInput):]))
                self.textCursor.setPosition(len(self.correctInput))
                self.textLabel.setTextCursor(self.textCursor)
            self.setWPM()
            self.setAccu()
            print(self.wrongChar)

        if self.inputContent == self.text:
            print("tapos na")
            accuDB = TinyDB("files/accuracy/accuracy.json")
            wpmDB = TinyDB("files/wpm/wpm.json")
            accuList = accuDB.search(User.name == player)[0]['accuracyList']
            wpmList = wpmDB.search(User.name == player)[0]['wpmList']
            if len(accuList) == 0:
                accuDB.update({'accuracy': self.accuracy, 'accuracyList': [self.accuracy]}, User.name == player)
            else:
                accuList.append(self.accuracy)
                accuracy = sum(accuList)/len(accuList)
                accuDB.update({'accuracy': accuracy, 'accuracyList': accuList}, User.name == player)
            if len(wpmList) == 0:
                wpmDB.update({'wpm': self.wordsPM, 'wpmList': [self.wordsPM]}, User.name == player)
            else:
                wpmList.append(self.wordsPM)
                wpm = sum(wpmList)/len(wpmList)
                wpmDB.update({'wpm': wpm, 'wpmList': wpmList}, User.name == player)
            print(accuDB.search(User.name == player))
            print(wpmDB.search(User.name == player))
            print(accuList)
            accuUp = accuDB.search(User.name == player)
            wpmUp = wpmDB.search(User.name == player)
            self.info.setHidden(False)
            self.textLabel.setReadOnly(True)
        self.textLabel.blockSignals(False)

stylesheet = """
QWidget {
    background-color: rgb(50, 52, 55);
}



QTextEdit {
    color: rgb(100, 102, 105);
    border: none;
}

QLabel {
    color: rgb(100, 102, 105);
}

QPushButton {
    border: none;
}

QPushButton#profile {
    color: #D1D0C5;

}

QPushButton#nextButton, QPushButton#restartButton {
    background-repeat: no-repeat;
}

QPushButton#nextButton {
    background-image: url(files/pictures/next.png);
}

QPushButton#restartButton {
    background-image: url(files/pictures/restart.png);
}

QPushButton#chooseParagraph:hover, QPushButton#chooseRandom:hover, QPushButton#login:hover, QPushButton#create:hover {
    color: #D1D0C5;
}
QPushButton#chooseParagraph:pressed, QPushButton#chooseRandom:pressed, QPushButton#login:pressed, QPushButton#create:pressed {
    color: #E2B714;
}

QPushButton#chooseParagraph, QPushButton#chooseRandom, QPushButton#login, QPushButton#create {
    color: rgb(100, 102, 105);
}

QTextEdit#UserTE, QTextEdit#PassTE {
    border: none;
    color: rgb(100, 102, 105);
}
"""    


app = QApplication(sys.argv)
app.setStyleSheet(stylesheet)
#win = LogIn()
#win = WindowPick()
win = Window("paragraph")
win.show()
sys.exit(app.exec_())