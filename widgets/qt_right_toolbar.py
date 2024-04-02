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
import core.yamaha as yam

class QTRightToolBar(qtw.QToolBar):

    def __init__(self, q_main_window):
        super().__init__(q_main_window)
        self.q_main_window = q_main_window
        self.setStyleSheet(self.q_main_window.styleSheet())
        self.setIconSize(qtc.QSize(48,48))
        self.setMinimumWidth(96)
        self.setMovable(False)
        self.icon_path = "./icons/"
        q_main_window.addToolBar(qtc.Qt.RightToolBarArea,self)
        self.current_active_button_group = "amp"
        self.current_active_button_item = "yam-00"
        self.active_button_color = "#e8904d"
        self.normal_button_color = "#777770"
        self.unit_name_list = ["alpha", "beta", "gamma", "delta"]
        self.action_dict = {}
        self.playback_is_paused = False
        self.unit_list = []
        # layout the buttons in the toolbar    

        # self.add_toolbar_spacer() 
        for unit in range(len(self.q_main_window.yam_ip_list)):
            item_name = f"unit-{unit:02d}"
            unit_d = {}
            unit_d['item'] = item_name
            unit_d['ip'] = self.q_main_window.yam_ip_list[unit]
            self.add_normal_toolbar_button("amp",item_name,"audio_video_receiver_48.png")
            unit_d['handle'] = yam.YamahaAmp(self.q_main_window.yam_ip_list[unit])
            unit_d['info'] = i = unit_d['handle'].get_info()
            unit_d['model_name'] = mn = i['model_name']
            unit_d['network_status'] = ns = unit_d['handle'].get_network_status()
            unit_d['network_name'] = nn = ns['network_name']
            unit_d['label'] = l = yamstyle.styled_label(self.q_main_window,nn,12)
            self.addWidget(l)
            self.unit_list.append(unit_d)
            print(f"Added Yamaha {mn} ({nn}).")
            # self.add_toolbar_spacer()
        # layout the buttons in the toolbar    
        self.add_unit_display() 
        self.select_button("amp","unit-00")


    def select_unit(self,unit:int):
        self.unit_display.setText(self.unit_list[unit]['model_name'].upper())
        self.q_main_window.yam = self.unit_list[unit]['handle']
        self.q_main_window.reset_frame()


    def add_toolbar_spacer(self):
        spacer = yamstyle.styled_spacer(self.q_main_window)
        self.addWidget(spacer)


    def add_unit_display(self):
        self.unit_display = yamstyle.styled_label(self.q_main_window,"Unit 1",18)
        self.unit_display.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter | qtc.Qt.AlignmentFlag.AlignVCenter)
        self.unit_display.setObjectName("UNIT")
        # self.unit_display.setFixedWidth(88)
        self.addWidget(self.unit_display)
    

    def add_normal_toolbar_button(self,group_name,item_name,icon_file):
        print(f"Adding '{group_name}'::'{item_name}'")
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
            self.select_button(group_name, item_name)            
            self.q_main_window.statusBar().showMessage(group_name.capitalize() + " " + item_name.lower() + " selected", 3000)
            if group_name != "amp":
                self.q_main_window.stacked_layout.setCurrentIndex(self.q_main_window.stacked_frame_indices[group_name][item_name]) 
                self.q_main_window.reset_frame_timer()

    def select_button(self, group_name, item_name):
        self.colorize_button(self.current_active_button_group, self.current_active_button_item, self.normal_button_color)
        self.colorize_button(group_name,item_name,self.active_button_color)
        self.current_active_button_group = group_name
        self.current_active_button_item = item_name  
        str_list = item_name.split('-') 
        unit = int(str_list[1])
        self.select_unit(unit)

    def show_input(self, input: str):
        self.input_display.setText(input)


    def show_paused(self, is_paused):
        self.playback_is_paused = is_paused
        if is_paused:
            self.colorize_button("playback","play",self.normal_button_color)
        else:
            self.colorize_button("playback","play",self.active_button_color)
