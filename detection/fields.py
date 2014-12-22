__author__ = 'sinisa'
import datetime

class Field():

    def __init__(self, image, x, y, h, w, minsize):
        self.image = image.crop(x, y, h, w)
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.minsize = minsize
        self.carPassing = False

    def crop_image(self, img):
        res = img
        res = res.crop(self.x, self.y, self.h, self.w)
        return res

    def detect(self, img):
        diff = self.crop_image(img) - self.image
        blobs = diff.findBlobs(minsize=self.minsize)
        if blobs:
            if not self.carPassing:
                self.carPassing = True
                return True
        else:
            self.carPassing = False
        return False

class Car():

    def __init__(self, hour, minute, second):
        self.start_time = datetime.datetime(hour=hour, minute=minute, second=second)


    def start_time(self):
        return self.start_time

    def end_time(self):
        pass

    def speed(self, framerate, distance):
        pass


class Counter():

    def __init__(self, cnt, framerate, hour, minute, second, distance):
        self.input_fields = []
        self.output_fields = []
        self.cnt = 0
        self.rate = 0
        self.framerate = framerate
        self.starttime = datetime.datetime(hour=hour, minute=minute, second=second)
        self.time = self.starttime
        self.moving_cars = []
        self.passed_cars = []
        pass

    def add_input_field(self, fld):
        self.input_fields.append(fld)

    def settime(self):
        if self.rate == 1:
            self.rate = 0
            self.time = self.starttime + datetime.timedelta(second=1)
        self.rate = self.rate + 1/self.framerate

    def detect(self, img):
        for f in self.input_fields:
            self.settime()
            if f.detect(img):
                self.cnt = self.cnt + 1
                self.moving_cars.append(Car(self.starttime))
        for f in self.output_fields:
            carNum = 0
            if f.detect(img):
                carNum = carNum + 1
                pass
