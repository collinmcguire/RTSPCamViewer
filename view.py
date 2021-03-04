from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
from threading import Thread

class RTSPVideo(QWidget):
    # Setup signal
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self,camera,parent=None):
        super(RTSPVideo,self).__init__(parent)

        self.rtspLink = cv2.VideoCapture(camera)

        # Start new thread to get camera stream
        self.thread = Thread(target=self.get_frames,args=())
        self.thread.dameon = True
        self.thread.start()

        # Create new label
        self.img_label = QLabel()

        # Connect signal to slot
        self.change_pixmap_signal.connect(self.update_image)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def get_frames(self):
        while True:
            ret, img = self.rtspLink.read()
            if ret:
                # Convert to proper format
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_img.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(300,300, Qt.KeepAspectRatio)
                # Emit imgage to signal
                self.change_pixmap_signal.emit(p)

    @pyqtSlot(QImage)
    def update_image(self,img):
        self.img_label.setPixmap(QPixmap.fromImage(img))

    def get_image_frame(self):
        return self.img_label

    def closeEvent(self, event):
        self.rtspLink.release()
        self.thread.stop()
        event.accept()

if __name__== '__main__':
    app = QApplication(sys.argv)

    # Setup the main window
    mainWindow = QMainWindow()
    mainWindow.setWindowTitle('IP Cam RTSP Stream')

    # Widget Setup
    camWidget = QWidget()

    # Layout Setup
    layout = QGridLayout()
    camWidget.setLayout(layout)
    mainWindow.setCentralWidget(camWidget)

    # Setup new cam streams
    cameras = ['rtsp://192.168.100.23:554/s1','rtsp://192.168.100.16:554/s1','rtsp://192.168.100.22:554/s1']

    for camera in cameras:
        # Get video feed going
        feed = RTSPVideo(camera)

        # Add to layout
        layout.addWidget(feed.get_image_frame())

    # Show to main window
    mainWindow.show()

    sys.exit(app.exec_())
