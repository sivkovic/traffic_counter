__author__ = 'sinisa'
import uuid
from SimpleCV import Color


class Field(object):

    def __init__(self, vid, x, y, w, h, frame=1, field_id=None):
        '''
        :param image: Whole image
        :param x: Coordinate x
        :param y: Coordinate y
        :param h: Height
        :param w: Width
        :param frame: Empty frame
        :param field_id: Field_id
        :return:
        '''
        self._id = field_id or uuid.uuid4()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = self.get_empty(vid, x, y, w, h, frame)

    @classmethod
    def get_empty(cls, vid, x, y, h, w, frame):
        img = vid.getImage()
        img = cls.crop_image(img, x, y, h, w)
        cnt = 1
        while(cnt < frame):
            img = vid.getImage()
        img = cls.crop_image(img, x, y, h, w)
        return img

    @classmethod
    def crop_image(cls, img, x, y, w, h):
        res = img
        res = res.crop(x, y, w, h)
        return res

    def detect(self, img):
        pass

    def show(self, img, color=Color.RED):
        img.drawRectangle(self.x, self.y, self.w, self.h, color=color)

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, d):
        pass

class Blob(Field):

    DEFAULT_SIZE = 50

    def __init__(self, image, x, y, w, h, frame=1, field_id=None, minsize=DEFAULT_SIZE):
        super(Blob, self).__init__(image, x, y, w, h, frame, field_id)
        self.minsize = minsize

    def detect(self, img):
        diff = self.crop_image(img, self.x, self.y, self.w, self.h) - self.image
        blobs = diff.findBlobs(minsize=self.minsize)

        if blobs:
            return True
        return False

    def to_dict(self):
        pass

    @classmethod
    def from_dict(self, d):
        pass


class Histogram(Field):

    DEFAULT_THRESHOLD = 0.5

    def __init__(self, vid, x, y, w, h, frame=1, field_id=None, threshold=DEFAULT_THRESHOLD):
        super(Histogram, self).__init__(vid, x, y, w, h, frame, field_id)
        self.threshold = threshold

    def detect(self, img):
        diff = self.crop_image(img, self.x, self.y, self.w, self.h) - self.image
        matrix = diff.getNumpy()
        mean = matrix.mean()

        if mean >= self.threshold:
            return True
        return False

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, d):
        return cls(d['vid'], d['cord']['x'], d['cord']['y'],
                   d['cord']['w'], d['cord']['h'],
                   d['cord'].get('frame', 1),
                   d.get('id', uuid.uuid4()),
                   d.get('threshold', cls.DEFAULT_THRESHOLD)
        )

