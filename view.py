from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

class RTSPVideo(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # IP Cam setup
        #BY = cv2.VideoCapture('rtsp://192.168.100.23:554/s1')
        #LR = cv2.VideoCapture('rtsp://192.168.100.22:554/s1')
        FY = cv2.VideoCapture('rtsp://192.168.100.16:554/s1')

        while self._run_flag:
            ret, img = FY.read()
            if ret:
                    self.change_pixmap_signal.emit(img)
        FY.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class ImageViewer(QWidget):
    # init
    def __init__(self):
        super().__init__()

        self.setWindowTitle('RTSP Stream')
        self.display_width = 640
        self.display_height = 480

        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        self.textlabel = QLabel('RTSP')

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textlabel)

        self.setLayout(vbox)

        self.thread = RTSPVideo()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self,event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self,img):
        qt_img = self.convert_cv_qt(img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self,img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__== '__main__':
    app = QApplication(sys.argv)

    vid = ImageViewer()
    vid.show()

    sys.exit(app.exec_())
