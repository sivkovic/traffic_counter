__author__ = 'sinisa'
import json
import time
import docopt
from SimpleCV import VirtualCamera, Color
from traffic import VERSION as version
from traffic.detection.fields import Counter, Field


height, width = 704, 576
#fieldDim1 = (530, 470, 180, 150)
fieldDim1 = (445, 333, 90, 60)

fieldDim2 = (530, 290, 100, 100)

def crop_image(image, x, y, h, w):
    res = image
    res = res.crop(x, y, h, w)
    return res


def open_vid(vid_path):
    vid = VirtualCamera(vid_path, 'video')
    empty = vid.getImage()
    return vid, empty

USAGE = '''
Usage:
    tcounter <video> -c <cfg> -o <out>
    tcounter --version
    Options:
  -c --config=<cfg>    Config file
  -o --output=<out>    Output file
     --version         Print version and exit.
'''

def main():
    try:
        args = docopt.docopt(USAGE, version=version, help=False)
        cfg = args.get('--config')
        out = args.get('--output')
        vid = args.get('<video>')


    except docopt.DocoptExit:
        print USAGE

def main_method():

    vid = VirtualCamera('../20141112-071614.mpeg', 'video')
    v = VirtualCamera('../20141112-071614.mpeg', 'video')
    field_1 = get_empty(v, fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3], 25)
    field_1.show()
    raw_input()

    background = vid.getImage()
    # field_1 = background
    # field_1 = crop_image(field_1, fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3])

    field_2 = background
    field_2 = crop_image(field_2, fieldDim2[0], fieldDim2[1], fieldDim2[2], fieldDim2[3])
    field_2.show()
    # background = crop_image(background, 0, 0, 50, 50)
    #field_1.show()
    #time.sleep(100)
    numOfCars = 0
    carPass = False
    while True:
        #time.sleep(1)
        current = vid.getImage()
        fld_1 = current
        fld_1 = crop_image(fld_1, fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3])
        #fld_1.show()
        #field_1.show()
        diff = fld_1 - field_1
        #diff.show()
        matrix = diff.getNumpy()
        mean = matrix.mean()
        print mean
        threshold = 10.0
        if mean >= threshold:
            if not carPass:
                carPass = True
                numOfCars=numOfCars+1
                print numOfCars
                current.drawRectangle(fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3], color=Color.RED)
        else:
            carPass = False
        current.show()

    # blobs = diff.findBlobs(minsize=120)
    #         if blobs:
    #             for blob in blobs:
    #                 rect=blob.boundingBox()
    #                 current.drawRectangle(rect[0], rect[1], rect[2], rect[3], color=Color.RED)
    #             if not carPass:
    #                 carPass = True
    #                 numOfCars=numOfCars+1
    #                 print numOfCars
    #             current.drawRectangle(fieldDim1[0], fieldDim1[1], fieldDim1[2], fieldDim1[3], color=Color.GREEN)
    #         else:
    #             carPass = False

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


def set_fields(config, vid_path):
    vid, empty = open_vid(vid_path)
    with open(config) as c:
        conf = json.load(c)
    fields = conf.get('fields')
    for f in fields:
        empty.drawRectangle(f['x'], f['y'], f['h'], f['w'], color=Color.RED)
    empty.show()
    raw_input()
    pass

def get_empty(vid, x, y, h, w, frame):
    img = vid.getImage()
    img = crop_image(img, x, y, h, w)
    cnt = 1
    while(cnt < frame):
        img = vid.getImage()
        img = crop_image(img, x, y, h, w)
        img.show()
        cnt = cnt+1
    print cnt
    return img


def frame_by_frame(config, vid_path):
    vid = VirtualCamera(vid_path, 'video')
    with open(config) as c:
        conf = json.load(c)
    fields = conf.get('inputs')
    img = vid.getImage()
    while img:
        for f in fields:
            img.drawRectangle(f['x'], f['y'], f['h'], f['w'], color=Color.RED)
        img.show()
        raw_input()
        img = vid.getImage()


def init(config, vid_path):
    counter = Counter(0, 25, 7, 16, 14, 0)
    with open(config) as c:
        conf = json.load(c)
    fields = conf.get('inputs')
    for f in fields:
        vid = VirtualCamera(vid_path, 'video')
        img = get_empty(vid, f['x'], f['y'], f['h'], f['w'], f["ref_frame"])
        counter.add_input_field(Field(img, f['x'], f['y'], f['h'], f['w'], f["minsize"], f.get('name')))
    return counter

if __name__ == '__main__':
    # main_method()
    # set_fields('config.json', '../20141112-071614.mpeg')
    # counter = init('detection/config.json', '../20141112-071614.mpeg')
    # vid = VirtualCamera('../20141112-071614.mpeg', 'video')
    # while True:
    #     current = vid.getImage()
    #     counter.detect(current)
    #     current.show()
    frame_by_frame('detection/config.json', '../20141112-071614.mpeg')
    #main()
