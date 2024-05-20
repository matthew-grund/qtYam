import os
import sys
import threading
import urllib

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWebEngineCore as qtweb

# local modules
import styles.qt_style_sheet as qt_style_sheet
import widgets.qt_central_widget as qt_central_widget
import widgets.qt_left_toolbar as qt_left_toolbar
import widgets.qt_bottom_toolbar as qt_bottom_toolbar
import widgets.qt_right_toolbar as qt_right_toolbar
import core.yamaha as yam


class QtYam(qtw.QMainWindow):

    def __init__(self):
        self.app = qtw.QApplication(sys.argv)
        qtw.QMainWindow.__init__(self) 
        self.title = "Yamaha Receiver"
        self.description = "Yamaha Receiver Interface"
        self.version_str = "0.7.3" 
        self.copyright_str = "(c) copyright 2024, Matthew Grund"
        self.setObjectName("Yamaha Qt Main Window")
        self.yam_ip_list = ['10.0.0.187', '10.0.0.216', '10.0.0.76']
        # self.yam_ip_list = ['10.0.0.187
        self.frame_timer_duration_ms = 3000
        self.yam = None
        self.last_art_url = ''
        self.click_global_pos = None
        self.show_debug = True
        self.debug("qtyam " + sys._getframe().f_code.co_name)

        self.screen = self.app.primaryScreen()
        self.screen_size =  self.screen.size()
        self.setWindowTitle(self.title)
        # self.resize(int(self.screen_size.width()*0.55),int(self.screen_size.height()*0.35))
        self.resize(936,420)
        self.app.setStyleSheet(qt_style_sheet.qss)
        self.frame_style = qtw.QFrame.Shape.Panel  # .Panel for designing, .NoFrame for a clean look    
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)

        # central widget is a stack of frames
        qt_central_widget.configure(self)
        qt_central_widget.setup(self)

        self.statusBar().showMessage("                          " + self.description + "  version " + self.version_str + "    " + self.copyright_str, 3000)
        
        # sync with the current amp status
        self.show_status()
        self.show_playback()

        # timer to reset the main panel to 
        self.frame_timer = qtc.QTimer()
        self.frame_timer.timeout.connect(self.reset_frame)
        self.frame_timer.start(3000)  

        # left toolbar has icon and buttons
        self.left_toolbar = qt_left_toolbar.QTLeftToolBar(self) 
        # bottom toolbar has buttons and text
        self.bottom_toolbar = qt_bottom_toolbar.QTBottomToolBar(self)
        # right toolbar has buttons and text
        self.right_toolbar = qt_right_toolbar.QTRightToolBar(self)

    def debug(self,msg):
        if self.show_debug:
            print(msg)

    def set_central_frame(self,group_name, item_name):
        self.debug(sys._getframe().f_code.co_name)
        self.statusBar().showMessage(group_name.capitalize() + " " + item_name.lower() + " selected", 3000)
        self.stacked_layout.setCurrentIndex(self.stacked_frame_indices[group_name][item_name]) 
        if group_name != "amp" or item_name != "playback":
            self.start_frame_timer()
        else:    
            self.cancel_frame_timer()


    def reset_frame(self):
        self.debug(sys._getframe().f_code.co_name)
        self.left_toolbar.toolbar_callback("amp","playback")
        self.bottom_toolbar.toolbar_callback("amp","playback")
        self.cancel_frame_timer()


    def cancel_frame_timer(self):
        self.debug(sys._getframe().f_code.co_name)
        if self.frame_timer:
            self.frame_timer.stop()
            self.frame_timer = None


    def start_frame_timer(self):
        if self.frame_timer:
            self.frame_timer.stop()
        self.frame_timer = qtc.QTimer()
        self.frame_timer.timeout.connect(self.reset_frame)
        self.frame_timer.start(self.frame_timer_duration_ms)  


    # init ui from amp statup  
    def show_status(self):
        self.debug(sys._getframe().f_code.co_name)
        if self.yam:
            ys = self.yam.get_status()
            # print(ys)
            if 'power' in ys:
                if ys['power'] == 'on':
                    self.left_toolbar.show_power(True)
                else:
                    self.left_toolbar.show_power(False)    
            if 'mute' in ys:
                if ys['mute']:
                    self.left_toolbar.show_mute(True)  
                else:
                    self.left_toolbar.show_mute(False)

            if 'volume' in ys:
                raw_volume = ys['volume']
                self.left_toolbar.show_raw_volume(raw_volume)   

            if 'actual_volume' in ys:
                actual_volume = ys['actual_volume']['value']
                units_str = ys['actual_volume']['unit']
                self.left_toolbar.show_actual_volume(actual_volume,units_str)

            if 'input_text' in ys:
                self.bottom_toolbar.show_input(ys['input_text'])

        # timer to sync state so that other conterollers - remotes, spotify, etc. can be tolerated
        self.status_timer = qtc.QTimer()
        self.status_timer.timeout.connect(self.show_status)
        self.status_timer.start(500)  


    def show_playback(self):
        self.debug(sys._getframe().f_code.co_name)
        if self.yam:
            yp = self.yam.get_now_playing()
            # print(yp)
            if 'artist' in yp and 'album' in yp and 'track' in yp:
                song = yp['track']
                album = yp['album']
                artist = yp['artist']
                self.update_song_album_artist(song,album,artist)

            if 'albumart_url' in yp:
                url = yp['albumart_url']
                art_url = "http://" + self.yam.get_ip_address() + url
                if art_url != self.last_art_url:
                    self.update_album_art(art_url)


        # timer to sync state so that other conterollers - remotes, spotify, etc. can be tolerated
        self.playback_timer = qtc.QTimer()
        self.playback_timer.timeout.connect(self.show_playback)
        self.playback_timer.start(500)  


    def update_album_art(self, art_url: str):
        self.debug(sys._getframe().f_code.co_name)
        if len(art_url):
            self.last_art_url = art_url
            # print(art_url)
            data = urllib.request.urlopen(art_url).read()
            image = qtg.QImage()
            image.loadFromData(data)
            art_width=self.album_art_label.width()
            self.statusBar().showMessage(f"Art width: {art_width}",3700)
            scaled_image = image.scaledToWidth(art_width, qtc.Qt.TransformationMode.SmoothTransformation)
            self.album_art_label.setPixmap(qtg.QPixmap(scaled_image))
    

    def update_song_album_artist(self, song: str, album: str, artist: str):
        self.debug(sys._getframe().f_code.co_name)
        # if len(song) > 31:
        #    song = song[:29] +'...'       
        self.playback_song_label.setText(song)

        # if len(album) > 40:
        #    album = album[:38] +'...'
        self.playback_album_label.setText(album)
        self.playback_artist_label.setText(artist)


    def mousePressEvent(self, event):
        self.click_global_pos = event.globalPosition().toPoint()


    def mouseMoveEvent(self, event):
        if self.click_global_pos is not None:
            delta = event.globalPosition().toPoint() - self.click_global_pos
            self.move(self.pos() + delta)
        self.click_global_pos = event.globalPosition().toPoint()


    def mouseReleaseEvent(self, event):
        self.click_global_pos = None


################################################
#
#  Start the QT app, which starts the Yamaha interface
#
################################################        
def main(args=None):
    # rclpy.init(args=args)
    yam = QtYam()
    yam.show()
    ret=yam.app.exec()
    sys.exit(ret)

if __name__ == '__main__':
    main()   
