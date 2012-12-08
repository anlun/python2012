# -*- coding: utf-8 -*-

__author__ = 'anlun'

import sys
import math
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
from TableInfo    import *
from PlayerInfo   import *
from Table        import *
from Turn         import *

from time         import sleep

class TableGui:
	card_height = 70
	card_width  = 50
	blind_size  = 45

	info_height = 150
	info_width  = 150
	name_height = 20

	center_x = 300
	center_y = 200

	table_card_coef = 1.5

	class PlayerInfoView:
		def __init__(self, player_info, scene, x, y):
			self.__player_info = player_info
			self.__scene = scene
			self.__pos = (x, y)

			self.__player_info.add_crl_cards(self)
			self.__player_info.add_crl_many(self)
			self.__player_info.add_crl_blind(self)
			self.__player_info.add_crl_ante(self)
			self.__player_info.add_crl_active_alive(self)

			self.__init_player_background()
			self.__init_player_name_view()
			self.__init_hand_card_view()
			self.__init_many_view()
			self.__init_ante_view()
			self.__init_blind_view()

		def __init_player_background(self):
			x = self.__pos[0]
			y = self.__pos[1]
			# self.__player_background = QGraphicsRectItem(x - 20, y - 20, TableGui.card_width * 3 + 40, TableGui.card_height + 70)
			self.__player_background = QGraphicsRectItem(x, y, TableGui.info_width, TableGui.info_height)

			self.__player_background.setBrush(Qt.yellow)
			self.__scene.addItem(self.__player_background)

		def __init_player_name_view(self):
			x = self.__pos[0]
			y = self.__pos[1]
			self.__name_view = QGraphicsTextItem(self.__player_info.name())
			self.__name_view.setPos(x, y)
			self.__scene.addItem(self.__name_view)

		def __init_hand_card_view(self):
			x = self.__pos[0] + TableGui.name_height
			y = self.__pos[1] + TableGui.name_height
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

			i = 0
			for card in self.__hand:
				if self.__player_info.is_hand_hidden:
					picture_path = card.image_path()
				else:
					picture_path = card.jacket_image_path()

				self.__hand_pixmaps[i].setPixmap(QPixmap(picture_path).scaledToHeight(TableGui.card_height))
				i += 1


		def blind_changed(self):
			blind = self.__player_info.blind()

			if blind == 0:
				self.__blind.setPixmap(QPixmap())
			elif blind == 1:
				self.__blind.setPixmap(QPixmap('images/littleblind.jpg').scaledToWidth(TableGui.card_width))
			else:
				self.__blind.setPixmap(QPixmap('images/bigblind.jpg').scaledToWidth(TableGui.card_width))

		def ante_changed(self):
			ante_text = 'FOLD'
			if not self.__player_info.is_folded():
				ante = self.__player_info.ante()
				ante_text = str(ante)
			self.__ante_text.setPlainText('Ante: ' + ante_text)

		def many_changed(self):
			many = self.__player_info.many()
			self.__many_text.setPlainText('Many: ' + str(many))

		def active_alive_changed(self):
			if not self.__player_info.is_alive():
				self.__player_background.setBrush(Qt.red)
				return
			if self.__player_info.is_active():
				self.__player_background.setBrush(Qt.green)
				return
			
			self.__player_background.setBrush(Qt.yellow)
			return

		def __init_many_view(self):
			x = self.__pos[0]
			y = self.__pos[1] + TableGui.name_height
			self.__many_text = QGraphicsTextItem('Many: ' + str(self.__player_info.many()))
			self.__many_text.setPos(x, y + TableGui.card_height)
			self.__scene.addItem(self.__many_text)

		def __init_ante_view(self):
			x = self.__pos[0]
			y = self.__pos[1] + TableGui.name_height
			self.__ante_text = QGraphicsTextItem('Ante: ' + str(self.__player_info.ante()))
			self.__ante_text.setPos(x, y + TableGui.card_height + TableGui.name_height)
			self.__scene.addItem(self.__ante_text)

		def __init_blind_view(self):
			x = self.__pos[0]
			y = self.__pos[1] + TableGui.name_height
			self.__blind = QGraphicsPixmapItem(QPixmap())
			if self.__player_info.blind() == 1:
				self.__blind = QGraphicsPixmapItem(QPixmap('images/littleblind.jpg').scaledToWidth(TableGui.blind_size))
			elif self.__player_info.blind() == 2:
				self.__blind = QGraphicsPixmapItem(QPixmap('images/bigblind.jpg').scaledToWidth(TableGui.blind_size))
			self.__blind.setPos(x + 1.8 * TableGui.card_width, y + TableGui.card_height * 1.1)
			self.__scene.addItem(self.__blind)		

	class OpenedCardView:
		def __init__(self, scene, table_info):
			self.__scene = scene
			self.__table_info = table_info

			table_info.add_crl_opened_cards(self)

			self.__card_view = []
			self.__card_view.append(QGraphicsPixmapItem(QPixmap()))
			self.__scene.addItem(self.__card_view[0])
			self.__card_view.append(QGraphicsPixmapItem(QPixmap()))
			self.__scene.addItem(self.__card_view[1])
			self.__card_view.append(QGraphicsPixmapItem(QPixmap()))
			self.__scene.addItem(self.__card_view[2])
			self.__card_view.append(QGraphicsPixmapItem(QPixmap()))
			self.__scene.addItem(self.__card_view[3])
			self.__card_view.append(QGraphicsPixmapItem(QPixmap()))
			self.__scene.addItem(self.__card_view[4])

			self.__card_view[0].setPos(TableGui.center_x - TableGui.card_width *     TableGui.table_card_coef, TableGui.center_y - TableGui.card_height / 2)
			self.__card_view[1].setPos(TableGui.center_x,                                                      TableGui.center_y - TableGui.card_height / 2)
			self.__card_view[2].setPos(TableGui.center_x + TableGui.card_width *     TableGui.table_card_coef, TableGui.center_y - TableGui.card_height / 2)
			self.__card_view[3].setPos(TableGui.center_x + TableGui.card_width * 2 * TableGui.table_card_coef, TableGui.center_y - TableGui.card_height / 2)
			self.__card_view[4].setPos(TableGui.center_x + TableGui.card_width * 3 * TableGui.table_card_coef, TableGui.center_y - TableGui.card_height / 2)

			self.opened_cards_changed()

		def opened_cards_changed(self):
			# clear
			for card_view in self.__card_view:
				card_view.setPixmap(QPixmap())

			i = 0
			for card in self.__table_info.opened_cards():
				self.__card_view[i].setPixmap(QPixmap(card.image_path()).scaledToHeight(TableGui.card_height * TableGui.table_card_coef))
				i += 1

	class BankView:
		def __init__(self, scene, table_info):
			self.__scene = scene
			self.__table_info = table_info

			self.__table_info.add_crl_bank(self)

			self.__bank_text = QGraphicsTextItem('Bank: %d' % table_info.bank())
			self.__bank_text.setPos(TableGui.center_x, TableGui.center_y + TableGui.card_height)
			self.__scene.addItem(self.__bank_text)

		def bank_changed(self):
			self.__bank_text.setPlainText('Bank: %d' % self.__table_info.bank())

	class DecisionBlock:
		btn_width  = 70
		btn_height = 25

		def __init__(self):
			pass

		def start(self, scene, type, x, y):
			# type must be 'Call' or 'Check'
			self.__scene = scene
			self.__type  = type

			self.__call_check_btn = QPushButton(type)
			self.__call_check_btn.setGeometry(x, y, self.btn_width, self.btn_height)
			self.__call_check_btn.setEnabled(False)
			self.__scene.addWidget(self.__call_check_btn)

			self.__fold_btn  = QPushButton('Fold')
			self.__fold_btn.setGeometry(x, y + self.btn_height, self.btn_width, self.btn_height)
			self.__fold_btn.setEnabled(False)
			self.__scene.addWidget(self.__fold_btn)

			self.__raise_btn = QPushButton('Raise:')
			self.__raise_btn.setGeometry(x + self.btn_width, y, self.btn_width, self.btn_height)
			self.__raise_btn.setEnabled(False)
			self.__scene.addWidget(self.__raise_btn)

			self.__raise_sum_input = QLineEdit()
			self.__raise_sum_input.setGeometry(x + self.btn_width * 2, y, self.btn_width, self.btn_height)
			self.__raise_sum_input.setEnabled(False)
			self.__scene.addWidget(self.__raise_sum_input)

			self.__allin_btn = QPushButton('All-in')
			self.__allin_btn.setGeometry(x + self.btn_width, y + self.btn_height, self.btn_width * 2, self.btn_height)
			self.__allin_btn.setEnabled(False)
			self.__scene.addWidget(self.__allin_btn)

			self.__fold_btn.clicked.connect(self.__fold_clicked)
			self.__call_check_btn.clicked.connect(self.__call_check_clicked)
			self.__allin_btn.clicked.connect(self.__allin_clicked)
			self.__raise_btn.clicked.connect(self.__raise_clicked)

		def __fold_clicked(self):
			self.deactivate(Turn('fold', 0))

		def __call_check_clicked(self):
			if self.__player.player_info().many() >= self.__min_value:
				self.deactivate(Turn('check or call', self.__min_value))

		def __allin_clicked(self):
			if self.__player.player_info().many() > 0:
				self.deactivate(Turn('allin', self.__player.player_info().many() + self.__player.player_info().ante()))

		def __raise_clicked(self):
			try:
				sum = int(self.__raise_sum_input.text())
				if sum >= self.__blind and sum <= self.__player.player_info().many():
					self.deactivate(Turn('raise', self.__player.player_info().ante() + sum))
			except ValueError:
				pass

		def activate(self, value, blind, player, func_to_call):
			self.__call_check_btn.setEnabled(True)
			self.__fold_btn.setEnabled(True)
			self.__raise_btn.setEnabled(True)
			self.__raise_sum_input.setEnabled(True)
			self.__allin_btn.setEnabled(True)

			self.__min_value = value
			self.__blind     = blind
			self.__player    = player
			self.__func_to_call = func_to_call

		def deactivate(self, turn_res):
			self.__call_check_btn.setEnabled(False)
			self.__fold_btn.setEnabled(False)
			self.__raise_btn.setEnabled(False)
			self.__raise_sum_input.setEnabled(False)
			self.__allin_btn.setEnabled(False)

			self.__func_to_call(turn_res)

	def __init__(self, table_info):
		self.__decision_block = TableGui.DecisionBlock()

		self.__table_info = table_info
		self.__table      = Table(table_info, self)

	def decision_block(self):
		return self.__decision_block

	def start(self):		
		self.__scene = QGraphicsScene()
		self.__view  = QGraphicsView(self.__scene)
		
		self.__table_image = QGraphicsPixmapItem(QPixmap('table.png'))
		self.__scene.addItem(self.__table_image)

		angle = math.pi * 2 / self.__table_info.player_count()
		radius_x = 400
		radius_y = 250
		cur_angle = math.pi / 2
		for player in self.__table_info.players():
			player_info_view = TableGui.PlayerInfoView(
				player
				, self.__scene
				, TableGui.center_x + radius_x * math.cos(cur_angle)
				, TableGui.center_y + radius_y * math.sin(cur_angle)
				)
			cur_angle += angle

		opened_card_view = TableGui.OpenedCardView(self.__scene, self.__table_info)
		bank_view = TableGui.BankView(self.__scene, self.__table_info)
		self.__decision_block.start(self.__scene, 'Call', 300, 320)

		self.__view.show()

	def __call__(self):
		self.__table.round()

if __name__ == '__main__':
	table_info = TableInfo()
	a = TableGui(table_info)
	a.start()