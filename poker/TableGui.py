# -*- coding: utf-8 -*-

__author__ = "anlun"
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from LogAnalyzer import *

class TableGui:
	card_height = 100
	card_width = 75

	def __init__(self, log_analyzer):
		self.__analyzer = log_analyzer
		

	def changeTable(self):
		self.__table_image.setPixmap(QPixmap("table1.png"))

	def add_player_info(self, x, y):
		# TODO: maybe delete previous elements

		# Background
		self.__player_background = QGraphicsRectItem(x - 10, y - 10, self.card_width * 3 + 20, self.card_height + 50)
		self.__player_background.setBrush(Qt.yellow)
		self.__scene.addItem(self.__player_background)

		# Hand cards
		self.__hand = self.__analyzer.hand_cards() 
		self.__hand_pixmaps = []

		cur_card_x = x
		for card in self.__hand:
			pixmap_item = QGraphicsPixmapItem(QPixmap(card.image_path()).scaledToHeight(self.card_height))
			pixmap_item.setPos(cur_card_x, y)
			self.__scene.addItem(pixmap_item)
			self.__hand_pixmaps.append(pixmap_item)

			cur_card_x += self.card_width

		# Bank size
		self.__bank_text = QGraphicsTextItem("Bank: " + str(self.__analyzer.many()))
		self.__bank_text.setPos(x, y + self.card_height)
		self.__scene.addItem(self.__bank_text)

		# Current ante
		self.__ante_text = QGraphicsTextItem("Ante: " + str(self.__analyzer.ante()))
		self.__ante_text.setPos(x, y + self.card_height + 20)
		self.__scene.addItem(self.__ante_text)

		# Blind
		self.__blind = QGraphicsPixmapItem(QPixmap())
		if self.__analyzer.cur_blind() == 1:
			self.__blind = QGraphicsPixmapItem(QPixmap('images/littleblind.jpg').scaledToWidth(self.card_width))
		elif self.__analyzer.cur_blind() == 2:
			self.__blind = QGraphicsPixmapItem(QPixmap('images/bigblind.jpg').scaledToWidth(self.card_width))
		self.__blind.setPos(x + 2 * self.card_width, y)
		self.__scene.addItem(self.__blind)

	def start(self):
		app = QApplication(sys.argv)
		
		self.__scene = QGraphicsScene()
		self.__view = QGraphicsView(self.__scene)
		
		self.__table_image = QGraphicsPixmapItem(QPixmap("table.png"))
		self.__scene.addItem(self.__table_image)

		self.add_player_info(100, 100)

		button = QPushButton("new game")
		self.__scene.addWidget(button)
		button.clicked.connect(self.changeTable)

		self.__view.show()
		return app.exec_()

if __name__ == "__main__":
	analyzer = LogAnalyzer("test")
	analyzer.set_hand_cards(Card(1, 10), Card(1, 9))
	a = TableGui(analyzer)
	a.start()
