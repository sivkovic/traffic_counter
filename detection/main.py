__author__ = 'sinisa'
import time
import copy
from SimpleCV import VirtualCamera, Color, Image
from geometry.geometry import Rect


height, width = 704, 576
fieldDim1 = (530, 470, 180, 150)
fieldDim2 = (530, 290, 100, 100)

def crop_image(image, x, y, h, w):
    res = image
    res = res.crop(x, y, h, w)
    return res

vid = VirtualCamera('/home/sinisa/Downloads/20141112-071614.mpeg', 'video')
background = vid.getImage()
field_1 = background
field_1 = crop_image(field_1, fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3])
field_2 = background
field_2 = crop_image(field_2, fieldDim2[0], fieldDim2[1], fieldDim2[2], fieldDim2[3])
field_2.show()
# background = crop_image(background, 0, 0, 50, 50)
#field_1.show()
#time.sleep(100)
numOfCars = 0
carPass = False
while True:
        #time.sleep(5)
        current = vid.getImage()
        fld_1 = current
        fld_1 = crop_image(fld_1, fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3])
        diff = fld_1 - field_1
        blobs = diff.findBlobs(minsize=80)
        if blobs:
            for blob in blobs:
                rect=blob.boundingBox()
                current.drawRectangle(rect[0], rect[1], rect[2], rect[3], color=Color.RED)
            if not carPass:
                carPass = True
                numOfCars=numOfCars+1
                print numOfCars
            current.drawRectangle(fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3], color=Color.GREEN)
        else:
            carPass = False

            #identify_blob(copy.deepcopy(blobs))
            #print len(blobs)
            # for blob in blobs:
            #     a=blob.meanColor()
            #     #print 'Mean color', a
            #     mc=(int(a[0]), int(a[1]), int(a[2]))
            #     colorDistance = blob.colorDistance()
            #     #print 'Color distance', colorDistance
            #     rect=blob.boundingBox()
            #     blob.draw()
            #     current.drawRectangle(rect[0], rect[1], rect[2], rect[3], color=Color.RED)
            # print '---------------------------------------------------------------'
        current.show()

