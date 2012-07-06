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
import sys

from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout, QSizePolicy
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import dbus
from dbus.mainloop.qt import DBusQtMainLoop

label = None #TODO not sure if I really need it global

class XMonadLogPlasmoid(plasmascript.Applet):
    label_signal = QtCore.pyqtSignal(str)
    session_bus = None
    _name_watcher = None

    BUSNAME = 'org.xmonad.Log'

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        self.setHasConfigurationInterface(False)

        self.applet.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.applet.setMaximumSize(sys.maxint, sys.maxint)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout.setMaximumSize(sys.maxint, sys.maxint)

        self.label = Plasma.Label(self.applet)

        self.layout.addItem(self.label)
        self.applet.setLayout(self.layout)

        self._setup_dbus()

    def _setup_dbus(self):
        if self.session_bus is None:
            self.session_bus = dbus.SessionBus()

        if not self.session_bus.name_has_owner('org.xmonad.Log'):
            self.label.setText("Waiting for XMonad...")
            self._name_watcher = self.session_bus.watch_name_owner(self.BUSNAME, self._bus_owner_changed)
        else:
            self._connect_to_signal()

    def _connect_to_signal(self, name=None):
        name = name or self.BUSNAME

        self._bus_proxy = self.session_bus.get_object(
            bus_name=name,
            object_path='/org/xmonad/Log',
            introspect=False)

        self._bus_proxy.connect_to_signal(
            handler_function=self.msg_receive,
            signal_name='Update',
            dbus_interface='org.xmonad.Log')

    def _bus_owner_changed(self, name):
        if name:
            self._connect_to_signal(name)

    def msg_receive(self, msg):
        self.label.setText(msg)

def CreateApplet(parent):
    DBusQtMainLoop(set_as_default=True)
    return XMonadLogPlasmoid(parent)

