import os
import sys

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWebEngineCore as qtweb


class QtYam(qtw.QMainWindow):

    def __init__(self):
        self.app = qtw.QApplication(sys.argv)
        qtw.QMainWindow.__init__(self) 
        self.title = "MapMap"
        self.description = "Simple Map for ROS"
        self.version_str = "0.3.3" 
        self.copyright_str = "(c) copyright 2023, Matthew Grund"
        self.screen = self.app.primaryScreen()
        self.screen_size =  self.screen.size()
        self.setWindowTitle(self.title)
        self.resize(int(self.screen_size.width()*0.70),int(self.screen_size.height()*0.30))
        self.app.setStyleSheet(qt_style_sheet.qss)
        self.frame_style = qtw.QFrame.Shape.Panel  # .Panel for designing, .NoFrame for a clean look    

        #self.setup_central_widget()
        #self.setup_left_toolbar()
        # keyboard_shortcuts.setup(self)
 





################################################
#
#  Start the QT app, which starts the ROS node
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