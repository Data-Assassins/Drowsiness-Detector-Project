import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

database={'admin': '1234', 'haya': '1234', 'ali': '1234'}

class mainWindow(QDialog):
    def __init__(self):
        super(mainWindow, self).__init__()
        loadUi('gui/guiHome.ui', self)
        self.setWindowTitle("Main Window")
        self.login.clicked.connect(self.login_clicked)
        self.signup.clicked.connect(self.signup_clicked)
    # login function will link to the login class then we show the login screen
    def login_clicked(self):
        # make object from login class
        login = loginWindow()
        # add it to the widget stack
        widget.addWidget(login)
        # to flip the screen to the login
        widget.setCurrentIndex(widget.currentIndex() + 1)
    # sign up function will link to the sign up class then we show the signup screen

    def signup_clicked(self):
        # make object from signup class
        signup = signupWindow()
        # add it to the widget stack
        widget.addWidget(signup)
        # to flip the screen to the signup
        widget.setCurrentIndex(widget.currentIndex() + 1)

class loginWindow(QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        loadUi('gui/guiLogin.ui', self)
        self.setWindowTitle("Login")
        # self.login.clicked.connect(self.login_clicked)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)
        self.backbutton.clicked.connect(self.back_button_function)
    # to handle the login button inside the login window
    def login_function(self):
        # get the username and password
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        # check if the username and password are correct and they are inside the database
        if username in database and database[username] == password:
            # if correct then show the main window
            print("Login Successful")
            user = userWindow()
            widget.addWidget(user)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif len(username) == 0 and len(password) == 0:
            # if username and password are empty show error message
            self.errorfield.setText("* Please enter your username and password")

        else:
            # if not correct then show the error message
            self.errorfield.setText("* Username or Password is incorrect")

    # to handle the back button inside the login window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)


# Create the signup class for the signup window
class signupWindow(QDialog):
    def __init__(self):
        super(signupWindow, self).__init__()
        loadUi('gui/guiSignup.ui', self)
        self.setWindowTitle("Signup")
        self.signup.clicked.connect(self.signup_function)
        self.backbutton.clicked.connect(self.back_button_function)

    # to handle the signup button inside the signup window
    def signup_function(self):
        # get the username and password
        username = self.usernamefield.text()
        password = self.passwordfield.text()
        passwordconfirm = self.passwordconfirmfield.text()

        # check if the username and password are correct and they are inside the database
        if password != passwordconfirm:
            # if not correct then show the error message
            self.errorfield.setText("* Password does not match") 

        elif username not in database and password == passwordconfirm:
            # if correct then show the main window
            print("Sign up Successful")
            # add the username and password to the database
            database[username] = password
            main = mainWindow()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif len(username) == 0 or len(password)==0 or len(passwordconfirm)== 0:
            # if username and password are empty show error message
            self.errorfield.setText("* Please enter your username and password")

        elif username in database:
            # if user name is found in the database
            self.errorfield.setText("* Username is Taken")

        else:
            # if not correct then show the error message
            self.errorfield.setText("* Something went Wrong")

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)
        
class userWindow(QDialog):
    def __init__(self):
        super(userWindow, self).__init__()
        loadUi('gui/guiUser.ui', self)
        self.setWindowTitle("User")
        self.start.clicked.connect(self.start_project_function) 
        self.report.clicked.connect(self.report_function) 
        self.backbutton.clicked.connect(self.back_button_function)
    # to handle the start button inside the user window
    # Here is the start for our program what functionality is implemented here
    def start_project_function(self):
        # our code here
        pass


    # to handle the report button inside the user window
    def report_function(self):
        report = reportWindow()
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)

class reportWindow(QDialog):
    def __init__(self):
        super(reportWindow, self).__init__()
        loadUi('gui/guiReport.ui', self)
        self.setWindowTitle("Report")
        self.backbutton.clicked.connect(self.back_button_function)

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() - 1)

# main
app = QApplication(sys.argv)
home = mainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(home)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting From The Application")
