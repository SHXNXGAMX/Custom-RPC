import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pypresence import Presence
from time import time
import sqlite3


class App(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('main.ui', self)
		self.FieldsStatus = True
		self.createDb()

		self.ButtonStart.clicked.connect(self.startRPC)
		self.ButtonStop.clicked.connect(self.stopRPC)
		self.ButtonLast.clicked.connect(self.loadData)


	def startRPC(self):
		self.createRPC(self.getInputData())
		self.blockFields()
		self.dbWrite()
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
		self.ButtonLast.setEnabled(self.FieldsStatus)

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
			self.RPC = Presence(f"{options['ClientID']}")
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

	def loadData(self):
		data = self.dbGet()

		self.ClientID.setText(str(data[0]))
		self.Details.setText(str(data[1]))
		self.State.setText(str(data[2]))
		self.LargeImageKey.setText(str(data[3]))
		self.LargeImageText.setText(str(data[4]))
		self.SmallImageKey.setText(str(data[5]))
		self.SmallImageText.setText(str(data[6]))
		self.ButtonName1.setText(str(data[7]))
		self.ButtonUrl1.setText(str(data[8]))
		self.ButtonName2.setText(str(data[9]))
		self.ButtonUrl2.setText(str(data[10]))
		self.Timestamp.setChecked(bool(data[11]))

	def dbWrite(self):
		
		sql = """UPDATE 'last_rpc' SET client_id = ?, details = ?, state = ?, large_image_key = ?, large_image_text = ?, small_image_key = ?, small_image_text = ?, button_1_name = ?, button_1_url = ?, button_2_name = ?, button_2_url = ?, "timestamp" = ?;"""
		options = self.getInputData()
		values = (
			options['ClientID'], 
			options['Details'], 
			options['State'], 
			options['LargeImageKey'], 
			options['LargeImageText'], 
			options['SmallImageKey'], 
			options['SmallImageText'], 
			options['ButtonName1'], 
			options['ButtonUrl1'], 
			options['ButtonName2'], 
			options['ButtonUrl2'], 
			int(options['Timestamp'])
			)

		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			data = cursor.execute(sql, values)
			db.commit()
			print(self.dbGet())

	def dbGet(self):
		sql = """SELECT * FROM 'last_rpc';"""

		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			data = cursor.execute(sql).fetchone()
			if data is None:
				values = ('1083727710901252156', 'CustomRPC UI', 'Lang: Python', 'custom_rpc_avatar', 'CustomRPC', 'shxnxgamx', 'by SHXNXGAMX', 'GitHub', 'https://github.com/SHXNXGAMX/Custom-RPC', '', '', 1)
				insertSql = """INSERT INTO 'last_rpc'('client_id', 'details', 'state', 'large_image_key', 'large_image_text', 'small_image_key', 'small_image_text', 'button_1_name', 'button_1_url', 'button_2_name', 'button_2_url', 'timestamp') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
				# 

				cursor.execute(insertSql, values)
				db.commit()

				data = cursor.execute(sql).fetchone()

		return data

	def createDb(self):
		sql = """CREATE TABLE IF NOT EXISTS "last_rpc" (
					"client_id"	TEXT DEFAULT '1083727710901252156',
					"details"	TEXT,
					"state"	TEXT,
					"large_image_key"	TEXT DEFAULT 'custom_rpc_avatar',
					"large_image_text"	TEXT DEFAULT 'CustomRPC',
					"small_image_key"	TEXT DEFAULT 'shxnxgamx',
					"small_image_text"	TEXT DEFAULT 'by SHXNXGAMX',
					"button_1_name"	TEXT,
					"button_1_url"	TEXT,
					"button_2_name"	TEXT,
					"button_2_url"	TEXT,
					"timestamp"	INTEGER DEFAULT 1
				);"""
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.executescript(sql)
			db.commit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	CustomRPC = App()
	CustomRPC.show()
	sys.exit(app.exec())