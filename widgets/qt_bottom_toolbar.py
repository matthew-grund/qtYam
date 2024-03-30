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
        self.setIconSize(qtc.QSize(42,42))
        self.setMinimumHeight(56)
        self.setMovable(False)
        self.icon_path = "./icons/"
        q_main_window.addToolBar(qtc.Qt.BottomToolBarArea,self)
        self.current_active_button_group = "amp"
        self.current_active_button_item = "playback"
        self.active_button_color = "white"
        self.normal_button_color = "#777770"
        self.action_dict = {}
        self.playback_is_paused = False

        # layout the buttons in the toolbar    
        self.add_toolbar_spacer() 
        self.add_toolbar_spacer()     
        self.add_normal_toolbar_button("amp","media","queue_music_96.png")
        self.add_input_display()
        self.add_toolbar_spacer()
        self.add_toolbar_spacer()        
        self.add_normal_toolbar_button("playback","previous","skip_previous_96.png")
        self.add_toolbar_spacer()
        self.add_active_toolbar_button("playback","play","play_circle_96.png")
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("playback","next","skip_next_96.png")
        self.add_toolbar_spacer()
        self.add_toolbar_spacer()
        self.add_toolbar_spacer()
        self.add_normal_toolbar_button("help","getting_started","help_outline_96.png")
        self.add_normal_toolbar_button("help","about","info_96.png")
        # self.add_normal_toolbar_button("playback","forward","list_alt_96.png")
        # self.add_normal_toolbar_button("playback","back","list_alt_96.png")    
        # self.add_normal_toolbar_button("help","getting_started","help_outline_96.png")
        # self.add_normal_toolbar_button("help","about","info_96.png")
        # self.add_toolbar_spacer()
        # self.add_normal_toolbar_button("map","config","settings_96.png")


    def add_toolbar_spacer(self):
        spacer = yamstyle.styled_spacer(self.q_main_window)
        self.addWidget(spacer)


    def add_input_display(self):
        self.input_display = yamstyle.styled_label(self.q_main_window,"Input",18)
        self.input_display.setFixedWidth(128)
        self.addWidget(self.input_display)
    

    def add_normal_toolbar_button(self,group_name,item_name,icon_file):
        i = self.normal_icon(self.icon_path + icon_file)
        a = qtg.QAction(i, item_name.title(), self)
        a.triggered.connect(lambda : self.toolbar_callback(group_name,item_name))
        self.addAction(a)
        if group_name not in self.action_dict:
            self.action_dict[group_name] = {}
        self.action_dict[group_name][item_name] = a  


    def add_active_toolbar_button(self,group_name,item_name,icon_file):
        i = self.active_icon(self.icon_path + icon_file)
        a = qtg.QAction(i, item_name.title(), self)
        a.triggered.connect(lambda : self.toolbar_callback(group_name,item_name))
        self.addAction(a)
        if group_name not in self.action_dict:
            self.action_dict[group_name] = {}
        self.action_dict[group_name][item_name] = a  


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
        if group_name == 'playback':
            self.control_callback(group_name, item_name) 
        else:
            self.select_button(group_name, item_name)
            self.q_main_window.statusBar().showMessage(group_name.capitalize() + " " + item_name.lower() + " selected", 3000)
            self.q_main_window.stacked_layout.setCurrentIndex(self.q_main_window.stacked_frame_indices[group_name][item_name]) 


    def control_callback(self, group_name, item_name):
        if group_name == "playback" and item_name == "play":
                self.q_main_window.yam.set_play(self.playback_is_paused)
                self.playback_is_paused = not self.playback_is_paused
                self.show_paused(self.playback_is_paused)
        if group_name == "playback" and item_name == "next":    
                self.q_main_window.yam.set_skip(True)   
        if group_name == "playback" and item_name == "previous":    
                self.q_main_window.yam.set_skip(False)    


    def select_button(self, group_name, item_name):
        self.colorize_button(self.current_active_button_group, self.current_active_button_item, self.normal_button_color)
        self.colorize_button(group_name,item_name,self.active_button_color)
        self.current_active_button_group = group_name
        self.current_active_button_item = item_name  


    def show_input(self, input: str):
        self.input_display.setText(input)


    def show_paused(self, is_paused):
        self.playback_is_paused = is_paused
        if is_paused:
            self.colorize_button("playback","play",self.normal_button_color)
        else:
            self.colorize_button("playback","play",self.active_button_color)
