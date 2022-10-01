import cv2
import numpy as np
import win32gui, win32ui, win32con
#import cv2 as cv for testing

class window_capture:

    #size of the screen and some prop
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, windowname= None):

        if windowname is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, windowname)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(windowname))
    
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # to look nicer
        border = 8
        titlebar = 30
        self.w = self.w - (border * 2)
        self.h = self.h - titlebar - border
        self.cropped_x = border
        self.cropped_y = titlebar

        # i cropped the img that with getting and move around a little so in order to keep a track of position
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y


    def getScreen(self):

        # img stuff
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resourses
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # wish i could tell u wat this does 
        # throw away useless data ?!?

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        #cv2.imshow('Roblox',img)
        return img

    # figures it out the name of ur windows
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
        return

    def getposition(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)



#wincap = window_capture('Roblox')
#wincap.getScreen()
#cv2.waitKey()
'''
while(True):
    wincar = window_capture('Roblox')
    cv.imshow('Computer Vision', wincar.getScreen())
    #points = visionFocus.find( screenshot, threshold=.50, debug_mode='rectangles')

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')
'''