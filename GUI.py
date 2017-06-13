import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Controller import Controller, CtrlEx

class CustomLine(QtWidgets.QListWidgetItem):
	def __init__(self, name, link):
		self.name = name
		self.link = link
		super(CustomLine, self).__init__(self.name)

	def getLink(self):
		return self.link

class MainWindow(QtWidgets.QWidget):
	def __init__(self, ctrl):
		super(MainWindow, self).__init__()
		self.ctrl = ctrl
		self.setGeometry(50,50,700,500)
		self.setWindowTitle("FreshSubs")
		self.setWindowIcon(QtGui.QIcon('fresh.png'))
		self.loadGUI()
		
	def loadGUI(self):
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.searchBox = QtWidgets.QLineEdit()
		self.mainLayout.addWidget(self.searchBox)

		self.languageBox = QtWidgets.QComboBox()
		self.languageBox.addItem("English")
		self.languageBox.addItem("Romanian")
		self.languageBox.currentIndexChanged.connect(self.loadSubs)
		self.mainLayout.addWidget(self.languageBox)

		self.listWidget = QtWidgets.QWidget()
		self.listLayout = QtWidgets.QHBoxLayout()
		self.listWidget.setLayout(self.listLayout)
		self.mainLayout.addWidget(self.listWidget)

		self.epList = QtWidgets.QListWidget()
		self.epList.selectionModel().selectionChanged.connect(self.loadSubs)
		self.listLayout.addWidget(self.epList)

		self.subsList = QtWidgets.QListWidget()
		self.listLayout.addWidget(self.subsList)

		self.btnWidget = QtWidgets.QWidget()
		self.btnLayout = QtWidgets.QHBoxLayout()
		self.btnWidget.setLayout(self.btnLayout)
		self.mainLayout.addWidget(self.btnWidget)

		self.searchBtn = QtWidgets.QPushButton("Search", self)
		self.searchBtn.clicked.connect(self.search_clicked)

		self.downloadBtn = QtWidgets.QPushButton("Download", self)
		self.downloadBtn.clicked.connect(self.download_sub)

		self.btnLayout.addWidget(self.searchBtn)
		self.btnLayout.addWidget(self.downloadBtn)

		self.show()

	def loadSubs(self):
		try:
			QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
			if(self.epList.currentRow() >= 0):
				self.subsList.clear()
				self.subs = self.ctrl.scrapSubs(self.epList.currentItem().getLink(), self.languageBox.currentText())
				for sub in self.subs:
					item = CustomLine(sub.getVersion() + " - " + sub.getLang() + " - " + sub.getImpaired(), sub.getLink())
					self.subsList.addItem(item)
		except CtrlEx as ex:
			QMessageBox.warning(self, 'Error', str(ex), QMessageBox.Ok)
		finally:
			QtWidgets.QApplication.restoreOverrideCursor()

	def search_clicked(self):
		try:
			QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
			self.epList.setCurrentRow(-1)
			self.epList.clear()
			self.subsList.clear()
			self.found = ctrl.scrapMedia(self.searchBox.text())
			for media in self.found:
				item = CustomLine(media.getName(), media.getLink())
				self.epList.addItem(item)
		except CtrlEx as ex:
			QMessageBox.warning(self, 'Error', str(ex), QMessageBox.Ok)
		finally:
			QtWidgets.QApplication.restoreOverrideCursor()

	def download_sub(self):
		try:
			QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
			link = self.subsList.currentItem().getLink()
			subName = self.epList.currentItem().text() + " - " + self.subsList.currentItem().text()
			self.ctrl.downloadSub(subName, link)
			QMessageBox.information(self, 'Success', "Subtitle was downloaded!", QMessageBox.Ok)
		except AttributeError as ex:
			QMessageBox.warning(self, 'Error', str(ex), QMessageBox.Ok)
		finally:
			QtWidgets.QApplication.restoreOverrideCursor()

app = QtWidgets.QApplication(sys.argv)
ctrl = Controller()
GUI = MainWindow(ctrl)
sys.exit(app.exec_())