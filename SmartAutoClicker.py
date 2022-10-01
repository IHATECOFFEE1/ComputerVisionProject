
import pyautogui as pa
import cv2 as cv
from time import sleep
import mouse



def WhereToClick():
    cv.waitKey(1000)
    x,y = pa.position()
    print('X= ',x , ' Y= ', y)
    
    return

def ClickHold():
    mouse.press(button='left')
    sleep(.50)
    mouse.release(button='left')

def ClickHold():
    mouse.click
    

cv.waitKey(3000) # u have 3 sec to find where to click

while(True):    
    ClickHold()
    sleep(3.5) # how long it takes for u to break a chest


   