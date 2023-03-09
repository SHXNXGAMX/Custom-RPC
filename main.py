import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('main.ui', self)
		self.FieldsStatus = True

		self.ButtonStart.clicked.connect(self.blockFields)
		self.ButtonStop.clicked.connect(self.blockFields)

	def blockFields(self):
		if self.FieldsStatus:
			self.FieldsStatus = False
		else:
			self.FieldsStatus = True

		self.ButtonName1.setEnabled(self.FieldsStatus)
		self.ButtonName2.setEnabled(self.FieldsStatus)
		self.ButtonUrl1.setEnabled(self.FieldsStatus)
		self.ButtonUrl2.setEnabled(self.FieldsStatus)
		self.Details.setEnabled(self.FieldsStatus)
		self.LargeImageKey.setEnabled(self.FieldsStatus)
		self.LargeImageText.setEnabled(self.FieldsStatus)
		self.SmallImageKey.setEnabled(self.FieldsStatus)
		self.SmallImageText.setEnabled(self.FieldsStatus)
		self.State.setEnabled(self.FieldsStatus)
		self.ClientID.setEnabled(self.FieldsStatus)
		self.Timestamp.setEnabled(self.FieldsStatus)

	def getInputData(self):
		options = {}
		options['timestamp'] = self.Timestamp.isChecked()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	CustomRPC = App()
	CustomRPC.show()
	sys.exit(app.exec())