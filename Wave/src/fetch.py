# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import config as cfg
import wave as wv
import threading
import multiprocessing
import Queue
import time
import os

# for multithread
queue_lock = threading.Lock()
code_queue = Queue.Queue()
threads = []
thread_id = 1

# for multiprocessing
proc_queue = multiprocessing.Queue()
procs = []
proc_id = 1

class ExportThread(threading.Thread):
    def __init__(self, thread_id, q, st, ed):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.q = q
        self.st = st
        self.ed = ed

    def run(self):
        print("Start thread {0}".format(self.thread_id))
        get_code_and_export(self.thread_id, self.q, self.st, self.ed)
        print("Exit thread {0}".format(self.thread_id))


def get_code_and_export(thread_id, q, start, end):
    while not q.empty():
        queue_lock.acquire()
        if not code_queue.empty():
            code = q.get()
            queue_lock.release()
            print("Thread {0} exports {1} from {2} to {3}".format(thread_id, code, start, end))
            export_ratio_table(code, start, end, thread_id)
        else:
            queue_lock.release()


class ExportProcess(multiprocessing.Process):
    def __init__(self, name, st, ed, q):
        multiprocessing.Process.__init__(self)
        self.name = str(name)
        self.st = st
        self.ed = ed
        self.q = q

    def run(self):
        print("Start process {0}".format(self.name))
        while not self.q.empty():
            code = self.q.get()
            print("    Process {0} exports {1} from {2} to {3}".format(self.name, code, self.st, self.ed))
            tries = 0
            while True:
                try:
                    export_ratio_table(code, self.st, self.ed, self.name)
                    break
                except Exception as e:
                    tries += 1
                    print("    Process {0} exception: {1}, try again for {2} times".format(self.name, e.message, tries))
                    time.sleep(1)
                    continue

        print("Exit process {0}".format(self.name))


def export_ratio_table(code, start, end, thread_id):
    # queue_lock.acquire()
    ts.set_token(cfg.get_datayes_key())
    mkt = ts.Market()

    # print("exporting " + code + " from " + start + " to " + end)
    st = time.time()
    df = mkt.MktEqud(ticker=code, beginDate=start, endDate=end,
                     field='ticker,tradeDate,preClosePrice,openPrice,highestPrice,lowestPrice,closePrice')
    print("        Thread {0} fetch online: {1}".format(thread_id, time.time()-st))
    # queue_lock.release()
    # df = ts.get_h_data(code, start, end)
    # print(df)
    wave_ratio_df = pd.DataFrame(columns=["max_ratio", "min_ratio"])

    for i, row in df.iterrows():
        dict = wv.calc_wave_ratio(row["preClosePrice"], row["openPrice"],
                                  row["highestPrice"], row["lowestPrice"])
        wave_ratio_df.loc[row["tradeDate"]] = dict

    st = time.time()
    idx_col = wv.calc_ratio_table_index_and_columns(max_ratio=0.03, min_ratio=-0.03)
    index, columns = idx_col["index"], idx_col["columns"]
    ratio_table = wv.calc_ratio_table(wave_ratio_df, index, columns)
    print("        Thread {0} calc ratio table: {1}".format(thread_id, time.time()-st))

    st = time.time()
    length_ratio_df = wv.calc_length_ratio(ratio_table, len(wave_ratio_df.index))
    print("        Thread {0} calc length ratio: {1}".format(thread_id, time.time()-st))

    # write csv
    st = time.time()
    ratio_table.to_csv(cfg.get_ratio_table_path(code, start, end))
    length_ratio_df.to_csv(cfg.get_length_ratio_path(code, start, end))
    # print("  save csv: {0}".format(time.time()-st))

    return length_ratio_df


if __name__ == "__main__":
    ts.set_token(cfg.get_datayes_key())
    eq = ts.Equity()
    df = eq.Equ(equTypeCD='A', listStatusCD='L', field='ticker')
    df['ticker'] = df['ticker'].map(lambda x: str(x).zfill(6))
    start, end = '20150901', '20160326'
    # thread can not make full use of cpu
    for i, row in df.iterrows():
        csv = cfg.get_ratio_table_path(row['ticker'], start, end)
        if os.path.exists(csv):
            print("{0}/{1} {2} exists.".format(i, len(df.index), row['ticker']))
            continue
        # code_queue.put(row['ticker'])
        # code_list.append(str(row['ticker']))
        proc_queue.put(row['ticker'])

    # for i in range(3):
    #     thread = ExportThread(thread_id, code_queue, start, end)
    #     thread.start()
    #     threads.append(thread)
    #     thread_id += 1
    #
    # get_code_and_export(0, code_queue, start, end)
    #
    # for t in threads:
    #     t.join()
    #
    # print("Exit main thread.")

    processes = 4
    for i in range(processes):
        p = ExportProcess(i+1, start, end, proc_queue)
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    print("Exit main")
