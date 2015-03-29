__author__ = 'sinisa'
import uuid
from SimpleCV import Color

class Field(object):

    def __init__(self, image, x, y, w, h, field_id=None):
        '''
        :param image: Whole image
        :param x: Coordinate x
        :param y: Coordinate y
        :param h: Height
        :param w: Width
        :param field_id: Field_id
        :return:
        '''
        self._id = field_id or uuid.uuid4()
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.image = self.crop_image(image, x, y, w, h)

    @classmethod
    def crop_image(cls, img, x, y, w, h):
        res = img
        res = res.crop(x, y, w, h)
        return res

    def detect(self, img):
        pass

    def show(self, img):
        img.drawRectangle(self.x, self.y, self.w, self.h, color=Color.RED)


class Blob(Field):

    DEFAULT_SIZE = 50

    def __init__(self, image, x, y, w, h, field_id=None, minsize=DEFAULT_SIZE):
        super(Blob, self).__init__(image, x, y, w, h, field_id)
        self.minsize = minsize

    def detect(self, img):
        diff = self.crop_image(img, self.x, self.y, self.w, self.h) - self.image
        blobs = diff.findBlobs(minsize=self.minsize)

        if blobs:
            return True
        return False

    @classmethod
    def from_dict(self):
        pass

    @classmethod
    def to_dict(self):
        pass


class Histogram(Field):

    DEFAULT_THRESHOLD = 0.5

    def __init__(self, image, x, y, w, h, field_id=None, threshold=DEFAULT_THRESHOLD):
        super(Histogram, self).__init__(image, x, y, w, h, field_id=None)
        self.threshold = threshold

    def detect(self, img):
        diff = self.crop_image(img, self.x, self.y, self.w, self.h) - self.image
        matrix = diff.getNumpy()
        mean = matrix.mean()

        if mean >= self.threshold:
            return True
        return False
