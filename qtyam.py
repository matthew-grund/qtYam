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
class QtYam(qtw.QMainWindow):

    def __init__(self):
        self.app = qtw.QApplication(sys.argv)
        qtw.QMainWindow.__init__(self) 
        self.title = "Yamaha Receivers"
        self.description = "Yamaha Receivers Interface"
        self.version_str = "0.3.3" 
        self.copyright_str = "(c) copyright 2024, Matthew Grund"
        self.screen = self.app.primaryScreen()
        self.screen_size =  self.screen.size()
        self.setWindowTitle(self.title)
        self.resize(int(self.screen_size.width()*0.70),int(self.screen_size.height()*0.30))
        self.app.setStyleSheet(qt_style_sheet.qss)
        self.frame_style = qtw.QFrame.Shape.Panel  # .Panel for designing, .NoFrame for a clean look    


        # central widget is a stack of frames
        qt_central_widget.configure(self)
        qt_central_widget.setup(self)
        #left toolbar has icons
        qt_left_toolbar.setup(self)
 





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