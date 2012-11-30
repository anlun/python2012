# -*- coding: utf-8 -*-

__author__ = 'anlun'

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from LogAnalyzer import *
from PlayerInfo import *

class TableGui:
	card_height = 100
	card_width = 75

	class MainPlayerInfoView:
		# TODO: add name label

		def __init__(self, player_info, scene, x, y):
			self.__player_info = player_info
			self.__scene = scene
			self.__pos = (x, y)

			self.__init_player_background()
			self.__init_hand_card_view()
			self.__init_bank_size_view()
			self.__init_ante_view()
			self.__init_blind_view()

		def __init_player_background(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__player_background = QGraphicsRectItem(x - 10, y - 10, TableGui.card_width * 3 + 20, TableGui.card_height + 50)
			self.__player_background.setBrush(Qt.yellow)
			self.__scene.addItem(self.__player_background)

		def __init_hand_card_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__hand = self.__player_info.hand_cards()
			self.__hand_pixmaps = []

			cur_card_x = x
			for card in self.__hand:
				pixmap_item = QGraphicsPixmapItem(QPixmap(card.image_path()).scaledToHeight(TableGui.card_height))
				pixmap_item.setPos(cur_card_x, y)
				self.__scene.addItem(pixmap_item)
				self.__hand_pixmaps.append(pixmap_item)

				cur_card_x += TableGui.card_width

		def __init_bank_size_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__bank_text = QGraphicsTextItem('Bank: ' + str(self.__player_info.many()))
			self.__bank_text.setPos(x, y + TableGui.card_height)
			self.__scene.addItem(self.__bank_text)

		def __init_ante_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__ante_text = QGraphicsTextItem('Ante: ' + str(self.__player_info.ante()))
			self.__ante_text.setPos(x, y + TableGui.card_height + 20)
			self.__scene.addItem(self.__ante_text)

		def __init_blind_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__blind = QGraphicsPixmapItem(QPixmap())
			if self.__player_info.blind() == 1:
				self.__blind = QGraphicsPixmapItem(QPixmap('images/littleblind.jpg').scaledToWidth(TableGui.card_width))
			elif self.__player_info.blind() == 2:
				self.__blind = QGraphicsPixmapItem(QPixmap('images/bigblind.jpg').scaledToWidth(TableGui.card_width))
			self.__blind.setPos(x + 2 * TableGui.card_width, y)
			self.__scene.addItem(self.__blind)			


	def __init__(self, log_analyzer):
		self.__analyzer = log_analyzer
		

	def changeTable(self):
		self.__table_image.setPixmap(QPixmap('table1.png'))

	def start(self):
		app = QApplication(sys.argv)
		
		self.__scene = QGraphicsScene()
		self.__view = QGraphicsView(self.__scene)
		
		self.__table_image = QGraphicsPixmapItem(QPixmap('table.png'))
		self.__scene.addItem(self.__table_image)

		playerInfoView = TableGui.MainPlayerInfoView(
			PlayerInfo('Vasya', [Card(1, 10), Card(1, 9)], 1000, 1, 200)
			,self.__scene
			, 100
			, 100
			)

		button = QPushButton('new game')
		self.__scene.addWidget(button)
		button.clicked.connect(self.changeTable)

		self.__view.show()
		return app.exec_()

if __name__ == '__main__':
	# analyzer = LogAnalyzer('test')
	analyzer = LogAnalyzer()
	# analyzer.set_hand_cards(Card(1, 10), Card(1, 9))
	a = TableGui(analyzer)
	a.start()
