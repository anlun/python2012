from PyQt4.QtGui  import *
from PyQt4.QtCore import *
import sys

from TableGui     import *
from TableInfo    import *

app = QApplication(sys.argv)

# # new game dialog
# msgBox = QMessageBox()
# msgBox.setText()

# if msgBox

table_info = TableInfo()
gui = TableGui(table_info)
gui.start()

QTimer.singleShot(20, gui)
# btn = QPushButton("new game")

# def start_game(bool_var):
# 	print 'aaa'
# 	gui()

# btn.clicked.connect(start_game)

# btn.show()

app.exec_()