# -*- coding: utf-8 -*-

import config as cfg
import tushare as ts
import numpy as np
import pandas as pd
import os
import threading
from datetime import datetime

class MV:
    '''

    '''
    def __init__(self, max_size=60*4, max_N=30):
        if max_size < 1:
            max_size = 1
        if max_N < 1:
            max_N = 1
        self.max_size = max_size
        self.max_N = min(max_size, max_N)
        self.q = []
        self.mvavg = [0.0 for x in range(self.max_size+1)]
        self.mvsum = [0.0 for x in range(self.max_size+1)]
        self.mvmin = [0.0 for x in range(self.max_size+1)]
        self.mvmax = [0.0 for x in range(self.max_size+1)]
        self.q_lock = threading.Lock()

    def push(self, num):
        if len(self.q) > self.max_size:
            raise BufferError("Too many numbers over {0}".format(self.max_size))
        self.q_lock.acquire()
        self.q.insert(0, num)
        self.__mvall()
        self.q_lock.release()

    def ma(self, N):
        if N < 1 or N > self.max_N:
            raise ValueError("invalid argument of N:{0}".format(N))
        return self.mvavg[N]

    def msum(self, N):
        if N < 1 or N > self.max_N:
            raise ValueError("invalid argument of N:{0}".format(N))
        return self.mvsum[N]

    def mmax(self, N):
        if N < 1 or N > self.max_N:
            raise ValueError("invalid argument of N:{0}".format(N))
        return self.mvmax[N]

    def mmin(self, N):
        if N < 1 or N > self.max_N:
            raise ValueError("invalid argument of N:{0}".format(N))
        return self.mvmin[N]

    def __mvall(self):
        if len(self.q) == 0:
            return

        for N in np.arange(1, self.max_N+1):
            self.__mvas(N)
            self.__mvmm(N)

    def __mvas(self, N):
        if N < 1 or N > self.max_N:
            raise ValueError("invalid argument of __mvas:{0}".format(N))

        l = len(self.q)
        if l == 0:
            return

        if l >= N:
            self.mvsum[N] = self.mvsum[N-1] + self.q[N-1]
            self.mvavg[N] = float(self.mvsum[N] / N)
        else:
            self.mvsum[N] = self.mvsum[N-1]
            self.mvavg[N] = self.mvavg[N-1]

    def __mvmm(self, N):
        if N < 1 or N > self.max_N:
            raise ValueError("invalid argument of __mvmm:{0}".format(N))

        l = len(self.q)
        if l == 0:
            return

        if N == 1:
            self.mvmin[1] = self.q[0]
            self.mvmax[1] = self.q[0]
        else:
            if l >= N:
                self.mvmin[N] = min(self.mvmin[N-1], self.q[N-1])
                self.mvmax[N] = max(self.mvmax[N-1], self.q[N-1])
            else:
                self.mvmin[N] = self.mvmin[N-1]
                self.mvmax[N] = self.mvmax[N-1]


class Dist:
    '''

    '''
    def __init__(self, interval=60, start_time = '9:30:00', end_time = '15:00:00'):
        if interval < 0:
            interval = 60

        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.q = []
        self.time_entry = self.get_time_entry(self.start_time, self.interval)
        self.last_time = ''

    @staticmethod
    def get_time_entry(time_str, interval):
        time_object = datetime.strptime(time_str, '%H:%M:%S')
        return (time_object.hour*3600 + time_object.minute*60 + time_object.second)/interval

    def reduce(self, time, num):
        if self.last_time == time:
            return None
        else:
            self.last_time = time

        new_time_entry = self.time_entry
        try:
            new_time_entry = self.get_time_entry(time, self.interval)
        except:
            return None

        if new_time_entry == self.time_entry:
            self.q.append(num)
            return None

        if len(self.q) == 0:
            return None

        sum = 0.0
        for x in self.q:
            sum += x
        avg = sum / len(self.q)
        del self.q[:]
        self.q.append(num)
        self.time_entry = new_time_entry
        return avg























































