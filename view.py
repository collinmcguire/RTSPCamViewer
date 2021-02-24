import cv2

LR = cv2.VideoCapture('rtsp://192.168.100.22:554/s1')
BY = cv2.VideoCapture('rtsp://192.168.100.23:554/s1')
FY = cv2.VideoCapture('rtsp://192.168.100.16:554/s1')

while True:
    _,frame1 = vid.read()
    cv2.imshow('rtsp',frame1)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

vid.release()
cv2.deystroyAllWindows()
