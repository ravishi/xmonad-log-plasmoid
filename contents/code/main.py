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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import os
import threading
import dbus
from dbus.mainloop.qt import DBusQtMainLoop

label = None #TODO not sure if I really need it global

class XMonadLogPlasmoid(plasmascript.Applet):

	label_signal = QtCore.pyqtSignal(str)
	session_bus = None

	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
		global label

		self.setHasConfigurationInterface(False)
#		self.setAspectRatioMode(Plasma.Square)
#
#		self.theme = Plasma.Svg(self)
#		self.theme.setImagePath("widgets/background")
#		self.setBackgroundHints(Plasma.Applet.DefaultBackground)

		self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
		label = Plasma.Label(self.applet)
		label.setText("Waiting for XMonad...")
		self.layout.addItem(label)
		self.applet.setLayout(self.layout)
		#self.resize(500,125)

		self.setup_dbus()
		self.label_signal.connect(update_label)

	def setup_dbus(self):
		self.session_bus = dbus.SessionBus()
		proxy = self.session_bus.get_object(
			bus_name='org.xmonad.Log',
			object_path='/org/xmonad/Log')

		self.session_bus.add_signal_receiver(
			handler_function=self.msg_receive,
			signal_name='Update',
			dbus_interface='org.xmonad.Log')

	def msg_receive(self, msg):
		self.label_signal.emit(msg)

def update_label(s):
	label.setText(s)

def CreateApplet(parent):
	DBusQtMainLoop(set_as_default=True)
	return XMonadLogPlasmoid(parent)

