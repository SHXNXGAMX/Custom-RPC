import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pypresence import Presence
from time import time

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('main.ui', self)
		self.FieldsStatus = True

		self.ButtonStart.clicked.connect(self.startRPC)
		self.ButtonStop.clicked.connect(self.stopRPC)

		self.createRPC(self.getInputData())

	def startRPC(self):
		self.blockFields()
		self.updateRPC()

	def stopRPC(self):
		self.blockFields()
		self.RPC.update()

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
		self.ButtonStart.setEnabled(self.FieldsStatus)
		self.ButtonStop.setEnabled(not self.FieldsStatus)
		self.ButtonClear.setEnabled(self.FieldsStatus)

	def getInputData(self) -> dict:
		options = {
			"ClientID": self.ClientID.text(),
			"Details": self.Details.text(),
			"State": self.State.text(),
			"Timestamp": self.Timestamp.isChecked(),
			"LargeImageKey": self.LargeImageKey.text(),
			"LargeImageText": self.LargeImageText.text(),
			"SmallImageKey": self.SmallImageKey.text(),
			"SmallImageText": self.SmallImageText.text(),
			"ButtonName1": self.ButtonName1.text(),
			"ButtonUrl1": self.ButtonUrl1.text(),
			"ButtonName2": self.ButtonName2.text(),
			"ButtonUrl2": self.ButtonUrl2.text()
		}
		return options

	def createRPC(self, options) -> bool:
		try:
			self.RPC = Presence("1083033486560067694")
			self.RPC.connect()
			return True

		except:
			return False

	def updateRPC(self):
		options = self.getInputData()
		self.RPCButtons = []

		for i in [1, 2]:
			if not not options[f"ButtonName{i}"]:
				button = {
					'label': str(options[f'ButtonName{i}']),
					'url': str(options[f'ButtonUrl{i}'])
				}
				self.RPCButtons.append(button)

		if options['Timestamp']:
			timestamp = time()

		self.RPC.update(
			details = str(options['Details']),
			state = str(options['State']),
			start = timestamp,
			buttons = self.RPCButtons,
			large_image = str(options['LargeImageKey']),
			large_text = str(options['LargeImageText']),
			small_image = str(options['SmallImageKey']),
			small_text = str(options['SmallImageText'])
		)
		print('RPC Started!')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	CustomRPC = App()
	CustomRPC.show()
	sys.exit(app.exec())