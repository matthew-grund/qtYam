#
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

class QTLeftToolBar(qtw.QToolBar):


    def __init__(self, q_main_window):
        super().__init__(q_main_window)
        self.q_main_window = q_main_window
        self.setStyleSheet(self.q_main_window.styleSheet())
        self.setIconSize(qtc.QSize(32,32))
        self.setMinimumWidth(96)
        self.setMovable(False)
        self.raw_volume_increment = 1
        self.icon_path = "./icons/"
        q_main_window.addToolBar(qtc.Qt.LeftToolBarArea,self)
        self.current_active_button_group = "amp"
        self.current_active_button_item = "playback"
        self.active_button_color = "#e8904d"
        self.normal_button_color = "#777770"
        self.on_button_color = "#e8904d"
        self.action_dict = {}
        self.current_actual_volume = 0
        self.current_raw_volume = 73
        self.volume_units_str = "counts"


        # toolbar elements
        self.add_app_logo("Yamaha-Logo.png")
        # layout the buttons in the toolbar    
        self.add_normal_toolbar_button("power","toggle","power_settings_new_96.png")
        # self.add_toolbar_spacer()
        self.add_volume_display()
        self.add_normal_toolbar_button("volume","up","volume_up_96.png")
        self.add_normal_toolbar_button("volume","down","volume_down_96.png")
        self.add_normal_toolbar_button("volume","mute","volume_off_96.png") 
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("amp","sound","equalizer_96.png")   
        self.power_is_on = False
        
        
    def add_toolbar_spacer(self):
        spacer = yamstyle.styled_spacer(self.q_main_window)
        self.addWidget(spacer)


    def add_app_logo(self, filename):
        self.app_label = yamstyle.styled_label(self.q_main_window,"YAMAHA",18)
        pixmap = qtg.QPixmap(self.icon_path + filename)
        painter = qtg.QPainter()
        painter.begin(pixmap)
        painter.setCompositionMode(qtg.QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), qtg.QColor("white"))
        painter.end()
        pixmap = pixmap.scaledToWidth(48,qtg.Qt.TransformationMode.SmoothTransformation)
        self.app_label.setPixmap(pixmap)
        self.addWidget(self.app_label)


    def add_normal_toolbar_button(self,group_name,item_name,icon_file):
        i = self.normal_icon(self.icon_path + icon_file)
        a = qtg.QAction(i, item_name.title(), self)
        a.triggered.connect(lambda : self.toolbar_callback(group_name,item_name))
        self.addAction(a)
        if group_name not in self.action_dict:
            self.action_dict[group_name] = {}
        self.action_dict[group_name][item_name] = a  


    def add_volume_display(self):
        self.volume_display = yamstyle.styled_label(self.q_main_window,"volume",14)
        self.addWidget(self.volume_display)


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
        return self.color_icon(filename,self.active_button_color)
    

    def normal_icon(self,filename):
        return self.color_icon(filename,self.normal_button_color)

    
    def toolbar_callback(self, group_name, item_name): 
        if group_name == 'volume' or group_name == 'power':
            self.control_callback(group_name, item_name) 
        else:
            self.select_button(group_name, item_name)
            self.q_main_window.statusBar().showMessage(group_name.capitalize() + " " + item_name.lower() + " selected", 3000)
            self.q_main_window.stacked_layout.setCurrentIndex(self.q_main_window.stacked_frame_indices[group_name][item_name]) 


    def control_callback(self, group_name, item_name):    
        self.q_main_window.statusBar().showMessage(group_name.capitalize() + " " + item_name.lower() + " clicked", 1000)
        if group_name == "power" and item_name == "toggle":
            if self.power_is_on:
                self.q_main_window.yam.set_power(False)
                self.show_power(False)
            else:
                self.q_main_window.yam.set_power(True)
                self.show_power(True)

        if group_name == "volume" and item_name == "mute":
            if self.volume_is_muted:
                self.q_main_window.yam.set_mute(False)
                self.show_mute(False)
            else:
                self.q_main_window.yam.set_mute(True)
                self.show_mute(True)

        if group_name == "volume" and item_name == "up":
                inc = self.raw_volume_increment
                self.q_main_window.yam.increment_volume(inc)
                self.show_raw_volume(self.current_raw_volume + inc)
                self.show_actual_volume(self.current_actual_volume + 0.5 * inc, self.volume_units_str)

        if group_name == "volume" and item_name == "down":
                inc = -1 * self.raw_volume_increment
                self.q_main_window.yam.increment_volume(inc)
                self.show_raw_volume(self.current_raw_volume + inc)
                self.show_actual_volume(self.current_actual_volume + 0.5 * inc,self.volume_units_str)


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


    def show_power(self, is_on: bool):
        self.power_is_on = is_on 
        if is_on:
            self.colorize_button("power", "toggle", self.on_button_color)
            self.show_mute(False)
        else:    
            self.colorize_button("power", "toggle", self.normal_button_color) 
            self.colorize_button("volume","up", self.normal_button_color)
            self.colorize_button("volume","down", self.normal_button_color)
            self.colorize_button("volume","mute", self.normal_button_color)
            self.toolbar_callback("help","about")
            self.volume_display.setText("- off -")


    def show_mute(self,is_muted: bool):
        self.volume_is_muted = is_muted
        if not self.power_is_on:
            return
        if is_muted:
            self.volume_display.setText("- mute -")
            self.colorize_button("volume","up", self.normal_button_color)
            self.colorize_button("volume","down", self.normal_button_color)
            self.colorize_button("volume","mute", self.on_button_color)
        else:
            self.show_actual_volume(self.current_actual_volume, self.volume_units_str)
            self.colorize_button("volume","up", self.on_button_color)
            self.colorize_button("volume","down", self.on_button_color)
            self.colorize_button("volume","mute", self.normal_button_color)


    def show_raw_volume(self,raw_volume: int):
        self.current_raw_volume = raw_volume
        # self.q_main_window.statusBar().showMessage(f"raw volume is {raw_volume}",300)
    

    def show_actual_volume(self, actual_volume: float, units_str):
        if not self.power_is_on:
            return
        self.current_actual_volume = actual_volume
        self.volume_units_str = units_str
        vol_str = str(actual_volume) + " " + units_str
        if not self.volume_is_muted:
            self.volume_display.setText(vol_str)    
