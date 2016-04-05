# -*- coding: utf-8 -*-

import config as cfg
import tushare as ts
import numpy as np
import pandas as pd
import os
import threading

class MV:
    '''

    '''
    def __init__(self, max_size=1):
        if max_size < 1:
            max_size = 1
        self.max_size = max_size + 1
        self.q = []
        self.mvavg = [0 for x in range(self.max_size)]
        self.mvsum = [0 for x in range(self.max_size)]
        self.mvmin = [0 for x in range(self.max_size)]
        self.mvmax = [0 for x in range(self.max_size)]
        self.q_lock = threading.Lock()

    def push(self, num):
        self.q_lock.acquire()
        self.q.insert(0, num)
        last = self.q[len(self.q)-1]
        if len(self.q) > self.max_size:
            self.q.pop()

        self.__mvall()
        self.q_lock.release()

    def ma(self, N):
        return self.mvavg[N-1]

    def mmax(self, N):
        return self.mvmax[N-1]

    def mmin(self, N):
        return self.mvmin[N-1]

    def __mvall(self):
        if len(self.q) == 0:
            return

        for N in np.arange(1, self.max_size+1):
            self.__mvas(N)
            self.__mvmm(N)

    def __mvas(self, N):
        if N < 1 or N > self.max_size:
            raise ValueError("invalid argument of __mvas:{0}".format(N))

        if len(self.q) == 0:
            return

        if N == 1:
            self.mvsum[N-1] = self.q[N-1]
            self.mvavg[N-1] = self.q[N-1]
        else:
            if len(self.q) >= N:
                self.mvsum[N-1] = self.mvsum[N-2] + self.q[N-1]
                self.mvavg[N-1] = self.mvsum[N-1] / (N - 1)
            else:
                self.mvsum[N-1] = self.mvsum[N-2]
                self.mvavg[N-1] = self.mvavg[N-2]

    def __mvmm(self, N):
        if N < 1 or N > self.max_size:
            raise ValueError("invalid argument of __mvmm:{0}".format(N))

        if len(self.q) == 0:
            return

        if N == 1:
            self.mvmin[N-1] = self.q[N-1]
            self.mvmax[N-1] = self.q[N-1]
        else:
            if len(self.q) >= N:
                self.mvmin[N-1] = min(self.mvmin[N-2], self.q[N-1])
                self.mvmax[N-1] = max(self.mvmax[N-2], self.q[N-1])
            else:
                self.mvmin[N-1] = self.mvmin[N-2]
                self.mvmax[N-1] = self.mvmax[N-2]
