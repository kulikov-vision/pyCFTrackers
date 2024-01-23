import numpy as np
import cv2
import time

from cftracker.mosse import MOSSE
from cftracker.mkcfup import MKCFup
from cftracker.strcf import STRCF
from cftracker.dat import DAT
from cftracker.config import staple_config,ldes_config,dsst_config,csrdcf_config,mkcf_up_config,mccth_staple_config

cap = cv2.VideoCapture('/media/s-kulikov/44F2BB9AF2BB8F24/my-work/FPV/DATA/123.mp4')
#tracker=MKCFup(config=mkcf_up_config.MKCFupLPConfig())
tracker=DAT()


left = top = -1
w = 40
h = 30
bbox = None
def get_click(event,x,y,flags,param):
    global left, top, right, bottom, bbox
    if event == cv2.EVENT_LBUTTONDOWN:
        left, top = x, y            
        bbox = (left-w//2, top-h//2, w, h)
cv2.namedWindow('image')
cv2.setMouseCallback('image',get_click)

ts = time.time()
skip = 0
i = 0
while True:
    i += 1
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    if i < skip:
        continue
    if not ret:
        break
        
    if left >= 0 and top >= 0:
        print('init', bbox)
        tracker.init(frame, bbox)
        left = top = -1
    
    if bbox is not None:
        bbox = tracker.update(frame)
        cv2.rectangle(frame, np.array(bbox).astype(int), (0, 0, 255), 1)    

    cv2.imshow('image', frame)
    delay = 34 - min(int(1000*(time.time() - ts)), 33)
    print(1000*(time.time() - ts))

    ts = time.time()
    if cv2.waitKey(delay) == 27:
        bbox = None