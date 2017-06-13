from sys import exit, argv
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QWidget, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout, QListWidget, QPushButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Controller import Controller, CtrlEx


class CustomLine(QListWidgetItem):
	def __init__(self, name, link):
		self.name = name
		self.link = link
		super(CustomLine, self).__init__(self.name)

	def getLink(self):
		return self.link

class MainWindow(QWidget):
	def __init__(self, ctrl):
		super(MainWindow, self).__init__()
		self.ctrl = ctrl
		self.setGeometry(50,50,700,500)
		self.setWindowTitle("FreshSubs")
		self.setWindowIcon(QIcon('fresh.png'))
		self.loadGUI()
		
	def loadGUI(self):
		self.mainLayout = QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.searchBox = QLineEdit()
		self.mainLayout.addWidget(self.searchBox)

		self.languageBox = QComboBox()
		self.languageBox.addItem("English")
		self.languageBox.addItem("Romanian")
		self.languageBox.currentIndexChanged.connect(self.loadSubs)
		self.mainLayout.addWidget(self.languageBox)

		self.listWidget = QWidget()
		self.listLayout = QHBoxLayout()
		self.listWidget.setLayout(self.listLayout)
		self.mainLayout.addWidget(self.listWidget)

		self.epList = QListWidget()
		self.epList.selectionModel().selectionChanged.connect(self.loadSubs)
		self.listLayout.addWidget(self.epList)

		self.subsList = QListWidget()
		self.listLayout.addWidget(self.subsList)

		self.btnWidget = QWidget()
		self.btnLayout = QHBoxLayout()
		self.btnWidget.setLayout(self.btnLayout)
		self.mainLayout.addWidget(self.btnWidget)

		self.searchBtn = QPushButton("Search", self)
		self.searchBtn.clicked.connect(self.search_clicked)

		self.downloadBtn = QPushButton("Download", self)
		self.downloadBtn.clicked.connect(self.download_sub)

		self.btnLayout.addWidget(self.searchBtn)
		self.btnLayout.addWidget(self.downloadBtn)

		self.show()

	def loadSubs(self):
		try:
			QApplication.setOverrideCursor(Qt.WaitCursor)
			if(self.epList.currentRow() >= 0):
				self.subsList.clear()
				self.subs = self.ctrl.scrapSubs(self.epList.currentItem().getLink(), self.languageBox.currentText())
				for sub in self.subs:
					item = CustomLine(sub.getVersion() + " - " + sub.getLang() + " - " + sub.getImpaired(), sub.getLink())
					self.subsList.addItem(item)
		except CtrlEx as ex:
			QMessageBox.warning(self, 'Error', str(ex), QMessageBox.Ok)
		finally:
			QApplication.restoreOverrideCursor()

	def search_clicked(self):
		try:
			QApplication.setOverrideCursor(Qt.WaitCursor)
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
			QApplication.restoreOverrideCursor()

	def download_sub(self):
		try:
			QApplication.setOverrideCursor(Qt.WaitCursor)
			link = self.subsList.currentItem().getLink()
			subName = self.epList.currentItem().text() + " - " + self.subsList.currentItem().text()
			self.ctrl.downloadSub(subName, link)
			QMessageBox.information(self, 'Success', "Subtitle was downloaded!", QMessageBox.Ok)
		except AttributeError as ex:
			QMessageBox.warning(self, 'Error', str(ex), QMessageBox.Ok)
		finally:
			QApplication.restoreOverrideCursor()

app = QApplication(argv)
ctrl = Controller()
GUI = MainWindow(ctrl)
exit(app.exec_())