import os
import sys

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWebEngineCore as qtweb

# local modules
import styles.qt_style_sheet as qt_style_sheet
import widgets.qt_central_widget as qt_central_widget
import widgets.qt_left_toolbar as qt_left_toolbar
import core.yamaha as yam

class QtYam(qtw.QMainWindow):

    def __init__(self):
        self.app = qtw.QApplication(sys.argv)
        qtw.QMainWindow.__init__(self) 
        self.title = "Yamaha Receiver"
        self.description = "Yamaha Receiver Interface"
        self.version_str = "0.3.3" 
        self.copyright_str = "(c) copyright 2024, Matthew Grund"
        self.screen = self.app.primaryScreen()
        self.screen_size =  self.screen.size()
        self.setWindowTitle(self.title)
        self.resize(int(self.screen_size.width()*0.70),int(self.screen_size.height()*0.45))
        self.app.setStyleSheet(qt_style_sheet.qss)
        self.frame_style = qtw.QFrame.Shape.Panel  # .Panel for designing, .NoFrame for a clean look    
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        # self.yam_ip = ['10.0.0.187', '10.0.0.216', '10.0.0.76']
        self.yam_ip = ['10.0.0.187']
        self.yam = yam.YamahaAmp(self.yam_ip[0])
        # central widget is a stack of frames
        qt_central_widget.configure(self)
        qt_central_widget.setup(self)
        #left toolbar has icons
        self.left_toolbar = qt_left_toolbar.QTLeftToolBar(self)    
        self.statusBar().showMessage(self.description + "  version " + self.version + "    " + self.copyright_str)
        self.init_status()


    # init ui from amp statup  
    def init_status(self):
        ys = self.yam.get_status()
        print(ys)
        if 'power' in ys:
            if ys['power'] == 'on':
                self.left_toolbar.show_power(True)
            else:
                self.left_toolbar.show_power(False)    


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



