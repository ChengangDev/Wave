# -*- coding: utf-8 -*-

import ConfigParser as cp
import datetime


def get_datayes_key():
    return "29f6bf6ac2349354f94506b932049dc50ca8817286f201bfe20d59b0b6ee8103"


wave_dir = "/home/chengang/Data/Wave"


def get_ratio_table_path(code, start, end):

    path = "{0}/{1}@{2}@{3}.ratio".format(wave_dir, code, start, end)
    return path


def get_length_ratio_path(code, start, end):

    path = "{0}/{1}@{2}@{3}.length".format(wave_dir, code, start, end)
    return path


share_dir = "/home/chengang/Data/Share"


def get_today_share_path(code):
    # print(datetime.date.today())
    # today = datetime.date.today()
    path = "{0}/{1}".format(share_dir, code)
    return path


if __name__ == "__main__":
    get_today_share_path('601318')