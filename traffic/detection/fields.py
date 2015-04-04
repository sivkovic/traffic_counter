__author__ = 'sinisa'
import datetime

class Field():

    def __init__(self, image, x, y, h, w, minsize, name=None):
        self.name = name
        self.image = image
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

    def detect_histogram(self, img):
        threshold = 0.8
        diff = self.crop_image(img) - self.image
        matrix = diff.getNumpy()
        mean = matrix.mean()
        print mean
        if mean >= threshold:
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
        self.starttime = datetime.datetime(2014, 1, 1, hour=hour, minute=minute, second=second)
        self.time = self.starttime
        self.moving_cars = []
        self.passed_cars = []
        pass

    def add_input_field(self, fld):
        self.input_fields.append(fld)

    def settime(self):
        if self.rate == self.framerate:
            self.rate = 0
            self.time = self.time + datetime.timedelta(seconds=1)
        self.rate = self.rate + 1

    def detect(self, img):
        for f in self.input_fields:
            img.show()
            self.settime()
            if f.detect_histogram(img):
                self.cnt = self.cnt + 1
                print(f.name + ": " + str(self.cnt))
                print(self.time)
                #self.moving_cars.append(Car(self.starttime))
        # for f in self.output_fields:
        #     carNum = 0
        #     if f.detect(img):
        #         carNum = carNum + 1
        #         pass
