# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QFileSystemWatcher
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import os
import threading

fifo_file = ["/home/igor/.cache/xmonad-log-plasmoid/pipe",]
label = None
f_obj = None #File object to read from fifo_file

class XMonadLogPlasmoid(plasmascript.Applet):

	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
		global label, f_obj

		self.setHasConfigurationInterface(False)
#		self.setAspectRatioMode(Plasma.Square)
#
#		self.theme = Plasma.Svg(self)
#		self.theme.setImagePath("widgets/background")
#		self.setBackgroundHints(Plasma.Applet.DefaultBackground)

		self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
		label = Plasma.Label(self.applet)
		label.setText("Hello world!")
		self.layout.addItem(label)
		self.applet.setLayout(self.layout)
		#self.resize(500,125)

		watcher = QFileSystemWatcher(fifo_file, self.applet)
		f_obj = open(fifo_file[0], 'r', 1)

		QtCore.QObject.connect(watcher, QtCore.SIGNAL("fileChanged(QString)"),
			update_label)

def update_label(s):
	label.setText(f_obj.readline())

def CreateApplet(parent):
	return XMonadLogPlasmoid(parent)
