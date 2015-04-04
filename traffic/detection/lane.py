__author__ = 'sinisa'

import uuid
import time


class Timer(object):

    def __init__(self, framerate):
        self.start_time = time.time()
        self.framerate = framerate
        pass


class Report(object):

    def __init__(self, in_time, lane_name=None):
        self.lane_name = lane_name or uuid.uuid4()
        self.in_time = in_time
        self.out_time = None
        self.distance = None

    @property
    def speed(self):
        return(self.distance / (self.in_time - self.out_time))

    def set_outtime(self, out_time):
        self.out_time = out_time
        if out_time > self.in_time:
            raise ValueError

    def __str__(self):
        return '{name}: {start_time} | {stop_time} | {speed}'.format(
            name=self.lane_name, start_time=self.in_time,
            stop_time=self.out_time, speed=self.speed)


class Lane(object):

    def __init__(self, input, output, timer):
        self.input = input
        self.passing_inp = False
        self.output = output
        self.passing_out = False
        self.cnt = 0
        self.lane_cnt = 0
        self.timer = timer

    def detect(self):
        if self.detect_pass(self.input, self.passing_inp):
            self.cnt = self.cnt + 1
        self.detect_pass(self.output, self.passing_out)
        pass

    def detect_pass(self, field, passing_flag):
        if field.detect():
            if not passing_flag:
                passing_flag = True
        else:
            if passing_flag:
                passing_flag = False
        return passing_flag

    def add_time(self):
        pass