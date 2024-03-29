#
#  ROS Home Qt UI
#
# Copyright 2022 Matthew Grund
#
# Licensed under the BSD 2 Clause license;
# you may not use this file except in compliance with the License.
#

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

import widgets.styled as mmw

class QTLeftToolBar(qtw.QToolBar):


    def __init__(self, q_main_window):
        super().__init__()
        self.q_main_window = q_main_window
        self.setIconSize(qtc.QSize(48,48))
        self.setMinimumWidth(96)
        self.setMovable(False)
        self.icon_path = "/data/home_ws/icons/"
        q_main_window.addToolBar(qtc.Qt.LeftToolBarArea,self)
        self.current_active_button_group = "map"
        self.current_active_button_item = "view"
        self.active_button_color = "#ffb75b"
        self.normal_button_color = "white"
        self.action_dict = {}
        # layout the buttons in the toolbar    
        # self.add_toolbar_spacer()
        self.add_toolbar_spacer()
        self.add_active_toolbar_button("map","view","map_96.png")  # these names correspond to frame names in central_widget.py
        # self.add_toolbar_spacer()
        self.add_normal_toolbar_button("map","layers","layers_96.png")
        # self.add_toolbar_spacer()
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("devices","view","gps_fixed_96.png")
        self.add_normal_toolbar_button("devices","messages","list_alt_96.png")
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("help","getting_started","help_outline_96.png")
        self.add_normal_toolbar_button("help","about","info_96.png")
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("map","config","settings_96.png")
        
         
    def add_toolbar_spacer(self):
        spacer = mmw.styled_spacer(self.q_main_window)
        self.addWidget(spacer)
        
        
    def add_normal_toolbar_button(self,group_name,item_name,icon_file):
        i = self.normal_icon(self.icon_path + icon_file)
        a = qtg.QAction(i, group_name.title(), self)
        a.triggered.connect(lambda : self.toolbar_callback(group_name,item_name))
        self.addAction(a)
        if group_name not in self.action_dict:
            self.action_dict[group_name] = {}
        self.action_dict[group_name][item_name] = a  


    def add_active_toolbar_button(self,group_name,item_name,icon_file):
        i = self.active_icon(self.icon_path + icon_file)
        a = qtg.QAction(i, group_name.title(), self)
        a.triggered.connect(lambda : self.toolbar_callback(group_name,item_name))
        self.addAction(a)
        if group_name not in self.action_dict:
            self.action_dict[group_name] = {}
        self.action_dict[group_name][item_name] = a  

        
    def color_icon(self, filename, color):
        pixmap = qtg.QPixmap(filename)
        painter = qtg.QPainter()
        painter.begin(pixmap)
        painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), qtg.QColor(color))
        painter.end()
        icon = qtg.QIcon(pixmap)
        return icon


    def active_icon(self,filename):
        return self.color_icon(filename,"#ffb75b")

        
    def normal_icon(self,filename):
        return self.color_icon(filename,"white")

    
    def toolbar_callback(self, group_name, item_name):   
        print("Left Toolbar: " + group_name + ":" + item_name)
        self.select_button(group_name, item_name)
        self.q_main_window.statusBar().showMessage(group_name + ":" + item_name)
        self.q_main_window.stacked_layout.setCurrentIndex(self.q_main_window.stacked_frame_indices[group_name][item_name]) 

    
    def select_button(self, group_name, item_name):
        self.colorize_button(self.current_active_button_group, self.current_active_button_item, self.normal_button_color)
        self.colorize_button(group_name,item_name,self.active_button_color)
        self.current_active_button_group = group_name
        self.current_active_button_item = item_name  

          
    def colorize_button(self, group_name, item_name, color):
        if group_name in self.action_dict:
            if item_name not in self.action_dict[group_name]:
                return
            a = self.action_dict[group_name][item_name]
            i = a.icon()
            pixy = i.pixmap(96)         
            painter = qtg.QPainter()
            painter.begin(pixy)
            painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixy.rect(), qtg.QColor(color))
            painter.end()
            icon = qtg.QIcon(pixy)
            a.setIcon(icon)