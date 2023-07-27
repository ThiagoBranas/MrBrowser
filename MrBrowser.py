# importing required libraries
import pyttsx3
import threading
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem



# main window
class MainWindow(QMainWindow):
	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		# creating an ico
		self.setWindowIcon(QIcon("Mrbrowser.ico"))

		# creating a geometry for program
		self.setGeometry(0, 0, 1400, 850)

		# creating a tab widget
		self.tabs = QTabWidget()

		#agree atribute
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setStyleSheet("QWidget { background-color: rgb(83, 83, 83); padding: 4px;}")

		self.tabs.setStyleSheet(".my-tabs { background-color: rgb(83, 83, 83); border: 2px solid; border-radius 1px; border-color: black; }")

		# making document mode true
		self.tabs.setDocumentMode(True)

		# adding action when double clicked
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		# adding action when tab is changed
		self.tabs.currentChanged.connect(self.current_tab_changed)
		
		# making tabs closeable
		self.tabs.setTabsClosable(True)
		
		self.tabs.setStyleSheet("QTabWidget { background-color: gray; border: 2px solid; border-radius: 1px; border-color: black; }  QTabBar::tab:selected { background-color: rgb(84, 84, 84); border: 2px solid; border-radius: 0px; border-color: black; font-size:13px; width: 195px; padding: 2px; height:30px; color: white; }")
		self.tabs.setStyleSheet("QTabBar::tab::not:selected { border: 4px; border-radius: 0px; border-color: black; background-color: rgb(84, 84, 84); font-size: 17px; width: 200px; height: 30px; padding: 2px; color: white;}")

		# adding action when tab close is requested
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		# making tabs as central widget
		self.setCentralWidget(self.tabs)
		# creating a status bar
		self.status = QStatusBar()
		# setting status bar to the main window
		self.setStatusBar(self.status)

		# creating a tool bar for navigation
		navtb = QToolBar("navegación")

		# adding tool bar tot he main window
		self.addToolBar(navtb)

		# creating back action
		back_btn = QAction("🢀", self)

		# setting status tip
		back_btn.setStatusTip("Volver a la página anterior")

		# adding action to back button
		# making current tab to go back
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		# adding this to the navigation tool bar
		navtb.addAction(back_btn)
		# similarly adding next button
		next_btn = QAction("🢂", self)
		next_btn.setStatusTip("Reenviar a la página siguiente")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		# similarly adding reload button
		reload_btn = QAction("↻", self)
		reload_btn.setStatusTip("Recargar pagina")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		# creating home action
		home_btn = QAction("Inicio", self)
		home_btn.setStatusTip("Ir al inicio")

		# adding action to home button
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		# adding a separator
		navtb.addSeparator()

		# creating a line edit widget for URL
		self.urlbar = QLineEdit()

		# adding action to line edit when return key is pressed
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding line edit to tool bar
		navtb.addWidget(self.urlbar)
		navtb.setStyleSheet("width:25%; height: 33px; cursor: pointer; font-size: 16,6px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; background-color: #1a1a1a;")
		# similarly adding stop action
		stop_btn = QAction("Parar", self)
		stop_btn.setStatusTip("Dejar de cargar la página actual")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)

		# creating first tab
		self.add_new_tab(QUrl('https://mrbrowserxz.000webhostapp.com/'), 'Homepage')
		# showing all the components

		# setting window title
		self.setWindowTitle("Mr browser - Navegacion")
		self.show()
		self.browser = QWebEngineView()
 


	# method for adding new tab
	def add_new_tab(self, qurl = None, label =""):

		# if url is blank
		if qurl is None:
			# creating a Mr browser url
			qurl = QUrl('https://mrbrowserxz.000webhostapp.com/')
		# creating a QWebEngineView object
		browser = QWebEngineView()

		# setting url to browser
		browser.setUrl(qurl)
		# setting tab index
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)
		# adding action to the browser when url is changed
		# update the url
		browser.urlChanged.connect(lambda qurl, browser = browser:
								self.update_urlbar(qurl, browser))

		# adding action to the browser when loading is finished
		# set the tab title
		browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.tabs.setTabText(i, browser.page().title()))

	# when double clicked is pressed on tabs
	def tab_open_doubleclick(self, i):

		# checking index i.e
		# No tab under the click
		if i == -1:
			# creating a new tab
			self.add_new_tab()

	# when tab is changed
	def current_tab_changed(self, i):

		# get the curl
		qurl = self.tabs.currentWidget().url()
		# update the url
		self.update_urlbar(qurl, self.tabs.currentWidget())

		# update the title
		self.update_title(self.tabs.currentWidget())
	# when tab is closed
	def close_current_tab(self, i):

		# if there is only one tab
		if self.tabs.count() < 2:
			# do nothing
			return

		# else remove the tab
		self.tabs.removeTab(i)

	

	# method for updating the title
	def update_title(self, browser):

		# if signal is not from the current tab
		if browser != self.tabs.currentWidget():
			# do nothing
			return

		# get the page title
		title = self.tabs.currentWidget().page().title()

		# set the window title
		self.setWindowTitle("% s - Mr browser" % title)

	# action to go to home
	def navigate_home(self):

		# go to google
		self.tabs.currentWidget().setUrl(QUrl("https://mrbrowserxz.000webhostapp.com/"))

	# method for navigate to url
	def navigate_to_url(self):

		# get the line edit text
		# convert it to QUrl object
		q = QUrl(self.urlbar.text())

		# if scheme is blank
		if q.scheme() == "":
			# set scheme
			q.setScheme("http")

		# set the url
		self.tabs.currentWidget().setUrl(q)
				
	# method to update the url
	def update_urlbar(self, q, browser = None):

		# If this signal is not from the current tab, ignore
		if browser != self.tabs.currentWidget():
			return

		# set text to the url bar
		self.urlbar.setText(q.toString())

		# set cursor position
		self.urlbar.setCursorPosition(0)
		self.urlbar.setStyleSheet("padding: 4px; background-color: white; color: black; font-size: 14px; height: 16px; border: 4px solid; border-radius: 16px; border-color: white;")
		# Configurar hilos

		

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidad de habla
engine.setProperty('volume', 0.9)  # Volumen de la voz

engine.say("Te damos la bienvenida a Mister browser, Por favor espere mientras el navegador se Inicia")

engine.runAndWait()

# creating a PyQ5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Mr browser")


# creating MainWindow object

window = MainWindow()
window.setStyleSheet("background-color: #2c2c2c; font-size: 14.5px; color: white;")
window.showMaximized()

# loop
app.exec_()

if __name__ == '__main__':
    # Creamos la aplicación
    app = QApplication(sys.argv)
    # Creamos la ventana principal
    window.show()
    # Ejecutamos la aplicación
    sys.exit(app.exec_())
