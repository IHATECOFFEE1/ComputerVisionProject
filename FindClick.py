import cv2 as cv
import numpy as np
#from recordingGameNotCap import window_capture

class FindWhereClick:

    target_img = None
    target_h = 0
    target_w = 0
    method = None

    def __init__(self, target_img_path, method = cv.TM_CCOEFF_NORMED):

        # gamescreenshot is in uint8 idk about target i think jpg and png are consider uint8
        self.target_img = cv.imread(target_img_path, cv.IMREAD_UNCHANGED)
        #print('Target type = ',type(self.target_img))

        self.target_w = self.target_img.shape[1]
        self.target_h = self.target_img.shape[0]

        self.method = method


    def find(self, GameShot_img, threshold=.5, debug_mode=None):

        # method use to read the img
        #self.target_img = self.target_img[:,:,:3]
        #self.target_img = np.ascontiguousarray(self.target_img)
        result = cv.matchTemplate( GameShot_img, self.target_img, self.method)

        # loc (x ,y )
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        #rectangles (x, y, width , height)
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]),int(loc[1]), self.target_w, self.target_h]
            # adds twice because your group rectangles functions wont count areas with only 1 rectangle
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        
        #print('Best match top left position: %s' % str(max_loc))
        #print('Best match confidence: %s' % max_val )
        points = []
        if len(rectangles):  
            #print('Found Target')


            line_color = (0,0,255)
            line_type = cv.LINE_4
            marker_type = cv.MARKER_CROSS
            marker_color = (0,0,255)

            for (x, y, w, h) in rectangles:

                center_x = x + int(w/2)
                center_y = y + int(y/2)
                #keep track of points
                points.append((center_x,center_y))

                if debug_mode == 'rectangles':
                
                    top_left = (x,y)
                    bottom_right = (x + w, y + h)

                    cv.rectangle(GameShot_img, top_left, bottom_right, line_color,line_type)
                elif debug_mode == 'points': 
                    cv.drawMarker( GameShot_img, (center_x , center_y), marker_color, marker_type, line_type)
        else:
            print('Target not found')

        if debug_mode:
            cv.imshow('Matches',GameShot_img)
            #cv.waitKey()
            #u = 1 + 1

        return points


'''
wincap = window_capture('Roblox')

screenshot = wincap.getScreen()


Mouse = FindWhereClick('camoChest.jpg')
print('Screeshot type = ',type(screenshot))
print()
print()
print()

Mouse.find(screenshot, threshold=.6, debug_mode='rectangles')
'''