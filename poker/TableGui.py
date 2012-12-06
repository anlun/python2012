# -*- coding: utf-8 -*-

__author__ = 'anlun'

import sys
import math
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from TableInfo import *
from PlayerInfo import *

class TableGui:
	card_height = 100
	card_width  = 75

	class PlayerInfoView:
		def __init__(self, player_info, scene, x, y):
			self.__player_info = player_info
			self.__scene = scene
			self.__pos = (x, y)

			self.__player_info.add_crl_cards(self)
			self.__player_info.add_crl_many(self)
			self.__player_info.add_crl_blind(self)
			self.__player_info.add_crl_ante(self)

			self.__init_player_background()
			self.__init_player_name_view()
			self.__init_hand_card_view()
			self.__init_bank_size_view()
			self.__init_ante_view()
			self.__init_blind_view()

		def __init_player_background(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__player_background = QGraphicsRectItem(x - 20, y - 20, TableGui.card_width * 3 + 40, TableGui.card_height + 70)
			self.__player_background.setBrush(Qt.green)
			self.__scene.addItem(self.__player_background)

		def __init_player_name_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__name_view = QGraphicsTextItem(self.__player_info.name())
			self.__name_view.setPos(x, y - 20)
			self.__scene.addItem(self.__name_view)

		def __init_hand_card_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__hand = self.__player_info.hand_cards()
			self.__hand_pixmaps = []

			cur_card_x = x
			for card in self.__hand:
				if not self.__player_info.is_hand_hidden():
					picture_path = card.image_path()
				else:
					picture_path = card.jacket_image_path()

				pixmap_item = QGraphicsPixmapItem(QPixmap(picture_path).scaledToHeight(TableGui.card_height))
				pixmap_item.setPos(cur_card_x, y)
				self.__scene.addItem(pixmap_item)
				self.__hand_pixmaps.append(pixmap_item)

				cur_card_x += TableGui.card_width

		def hand_cards_changed(self):
			self.__hand = self.__player_info.hand_cards()

			for card in self.__hand:
				if self.__player_info.is_hand_hidden:
					picture_path = card.image_path()
				else:
					picture_path = card.jacket_image_path()

				self.__hand_pixmaps[i].setPixmap(QPixmap(picture_path).scaledToHeight(TableGui.card_height))


		def blind_changed(self):
			blind = self.__player_info.blind()

			if blind == 0:
				self.__blind.setPixmap(QPixmap())
			elif blind == 1:
				self.__blind.setPixmap(QPixmap('images/littleblind.jpg').scaledToWidth(TableGui.card_width))
			else:
				self.__blind.setPixmap(QPixmap('images/bigblind.jpg').scaledToWidth(TableGui.card_width))

		def ante_changed(self):
			ante = self.__player_info.ante()
			self.__ante_text.setPlainText('Ante: ' + str(ante))

		def many_changed(self):
			many = self.__player_info.many()
			self.__ante_text.setPlainText('Bank: ' + str(ante))

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

	def __init__(self, table_info):
		self.__table_info = table_info

	def changeTable(self):
		self.__table_image.setPixmap(QPixmap('table1.png'))

	def start(self):
		app = QApplication(sys.argv)
		
		self.__scene = QGraphicsScene()
		self.__view = QGraphicsView(self.__scene)
		
		self.__table_image = QGraphicsPixmapItem(QPixmap('table.png'))
		center_x = 300
		center_y = 200

		self.__scene.addItem(self.__table_image)

		angle = math.pi * 2 / self.__table_info.player_count()
		radius_x = 450
		radius_y = 300
		cur_angle = math.pi / 2
		for player in self.__table_info.players():
			playerInfoView = TableGui.PlayerInfoView(
				player
				, self.__scene
				, center_x + radius_x * math.cos(cur_angle)
				, center_y + radius_y * math.sin(cur_angle)
				)
			cur_angle += angle

		button = QPushButton('new game')
		self.__scene.addWidget(button)
		button.clicked.connect(self.changeTable)

		self.__view.show()
		return app.exec_()

if __name__ == '__main__':
	table_info = TableInfo()
	a = TableGui(table_info)
	a.start()
