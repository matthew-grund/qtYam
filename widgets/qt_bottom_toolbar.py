#  Yamaha app
#
# Copyright 2024 Matthew Grund
#
# Licensed under the BSD 2 Clause license;
# you may not use this file except in compliance with the License.
#

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

import widgets.styled as yamstyle

class QTBottomToolBar(qtw.QToolBar):

    def __init__(self, q_main_window):
        super().__init__(q_main_window)
        self.q_main_window = q_main_window
        self.setStyleSheet(self.q_main_window.styleSheet())
        self.setIconSize(qtc.QSize(48,48))
        self.setMinimumWidth(96)
        self.setMovable(False)
        self.raw_volume_increment = 1
        self.icon_path = "./icons/"
        q_main_window.addToolBar(qtc.Qt.LeftToolBarArea,self)
        self.current_active_button_group = "map"
        self.current_active_button_item = "view"
        self.active_button_color = "#e8904d"
        self.normal_button_color = "#777770"
        self.on_button_color = "#e8904d"
        self.action_dict = {}

        # layout the buttons in the toolbar    
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("playback","previous","power_settings_new_96.png")
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("volume","up","volume_up_96.png")
        self.add_normal_toolbar_button("volume","down","volume_down_96.png")
        self.add_normal_toolbar_button("volume","mute","volume_off_96.png")
        # self.add_normal_toolbar_button("playback","forward","list_alt_96.png")
        # self.add_normal_toolbar_button("playback","back","list_alt_96.png")    
        # self.add_normal_toolbar_button("help","getting_started","help_outline_96.png")
        # self.add_normal_toolbar_button("help","about","info_96.png")
        # self.add_toolbar_spacer()
        # self.add_normal_toolbar_button("map","config","settings_96.png")


    def add_toolbar_spacer(self):
        spacer = yamstyle.styled_spacer(self.q_main_window)
        self.addWidget(spacer)