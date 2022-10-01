import cv2 as cv
import numpy as np
import os
from time import time, sleep
from recordingGameNotCap import window_capture
from FindClick import FindWhereClick
import pyautogui
from threading import Thread


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# init window capture
wincap = window_capture('Roblox')
# init find where to click

visionFocus = FindWhereClick('camoChestwithSky.jpg')

isbotOn = False
def bot_action(points):
    
    if len(points) > 0:
        targets = wincap.getposition(points[0])
        pyautogui.moveTo(x=targets[0],y=targets[1])
        pyautogui.click()
        sleep(1)
        #pyautogui.moveTo(100,100)

        global isbotOn
        isbotOn = False
    return


loop_time = time()
while(True):

    screenshot = wincap.getScreen()

    #cv.imshow('Computer Vision', screenshot)
    points = visionFocus.find( screenshot, threshold=.55, debug_mode='rectangles')

    if not isbotOn:
        isbotOn = True
        t = Thread(target=bot_action, args=(points,))
        t.start()



    print('FPS {}'.format( int(1/ (time() - loop_time))))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')