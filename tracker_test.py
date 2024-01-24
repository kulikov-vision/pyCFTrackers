import numpy as np
import cv2
import time

from lib.utils import get_img_list,get_ground_truthes,APCE,PSR
from cftracker.mosse import MOSSE
from cftracker.csk import CSK
from cftracker.kcf import KCF
from cftracker.cn import CN
from cftracker.dsst import DSST
from cftracker.staple import Staple
from cftracker.dat import DAT
from cftracker.eco import ECO
from cftracker.bacf import BACF
from cftracker.csrdcf import CSRDCF
from cftracker.samf import SAMF
from cftracker.ldes import LDES
from cftracker.mkcfup import MKCFup
from cftracker.strcf import STRCF
from cftracker.mccth_staple import MCCTHStaple
from lib.eco.config import otb_deep_config,otb_hc_config
from cftracker.config import staple_config,ldes_config,dsst_config,csrdcf_config,mkcf_up_config,mccth_staple_config

cap = cv2.VideoCapture('/media/s-kulikov/44F2BB9AF2BB8F24/my-work/FPV/DATA/123.mp4')
#tracker=DAT()  #SUPER FAST 300fps
tracker=Staple(config=staple_config.StapleConfig()) #FAST 100fps
#tracker=MKCFup(config=mkcf_up_config.MKCFupLPConfig()) #MAYBE   40-50 pfs

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
    
    ts0 = time.time()
    if bbox is not None:
        bbox = tracker.update(frame)
        cv2.rectangle(frame, np.array(bbox).astype(int), (0, 0, 255), 1)    

    cv2.imshow('image', frame)
    delay = 34 - min(int(1000*(time.time() - ts)), 33)    

    ts = time.time()
    print(1000*(ts - ts0))
    if cv2.waitKey(delay) == 27:
        bbox = None