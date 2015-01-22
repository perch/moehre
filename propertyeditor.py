import string
from collections import namedtuple

from PyQt5 import QtCore, QtWidgets, QtGui, uic

def camelCaseToWords(text):
	words = ""
	for char in text:
		if not char in string.ascii_uppercase:
			words += char
		else:
			words += " " + char.lower()
	return words.strip()
	
Property = namedtuple("Property", ["name", "type", "value"])

class PropertyWidget(QtWidgets.QTableWidget):
	itemRolePropertyName = QtCore.Qt.UserRole + 1
	itemRolePropertyType = QtCore.Qt.UserRole + 2
	
	def __init__(self, parent=None):
		QtWidgets.QTableWidget.__init__(self, parent)
		
		self.setColumnCount(2)
		self.setHorizontalHeaderLabels(["Property", "Value"])
		
		self.itemChanged.connect(self.propertyChanged)
		
		self._currentList = None
		
	def loadProperties(self, properties):
		self.clearContents()
		
		self._currentList = properties
		self.setRowCount(len(self._currentList))
		
		for i, (_, property) in enumerate(self._currentList.items()):
		
		
			itemName = QtWidgets.QTableWidgetItem(camelCaseToWords(property.name))
			itemName.setFlags(itemName.flags() & ~QtCore.Qt.ItemIsEditable)
			self.setItem(i, 0, itemName)
			
			itemValue = QtWidgets.QTableWidgetItem(str(property.value))
			itemValue.setData(self.itemRolePropertyName, property.name)
			itemValue.setData(self.itemRolePropertyType, property.type)
			self.setItem(i, 1, itemValue)
						
		self.verticalHeader().hide()
		self.resizeColumnsToContents()
		
	def propertyChanged(self, item):
		name = item.data(self.itemRolePropertyName)
		type = item.data(self.itemRolePropertyType)
		if name and type:
			value = type(item.text())
			self._currentList[name] = Property(name=name, type=type, value=value)
				
				
				