import cv2
import numpy as np

# kamera aç
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# bir tane frame oku
ret, frame = cap.read()

if ret == False:
    print("uyarı")
    
# detection (tespit etme)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_rects = face_cascade.detectMultiScale(frame)

(face_x, face_y, w, h) = tuple(face_rects[0])
track_window = (face_x, face_y, w, h) # meanshift algoritması girdisi

# region of interest (tespit eilen kutucuğun içerisi)
roi = frame[face_y:face_y + h, face_x:face_x + w] #roi = face

hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV )

roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0,180]) # takip için histogram gerekli
cv2.normalize(roi_hist , roi_hist, 0,255,cv2.NORM_MINMAX)
# takip icin gerekli durdurma kriterleri
# count = hesaplanacak maksimum oge sayısı
# eps = degisiklik (epsilon)
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5, 1 )

while True:
    ret, frame = cap.read()
    
    if ret:
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # histogramı bir goruntude bulmak için kullnıyoruz
        # piksel karşılaştırma
        
        dst = cv2.calcBackProject([hsv], channels = [0], hist= roi_hist , ranges = [0,180], scale= 1)

        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        
        x,y,w,h = track_window
        
        img2 = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),5)
        
        cv2.imshow("takip", img2)
        
        if cv2.waitKey(1) & 0XFF == ord("q"): break
            
cap.release()
cv2.destroyAllWindows()
        


























