# -*- coding: utf-8 -*-
import unittest
import wave as wv
import pandas as pd



class TestWave(unittest.TestCase):

    def test_calc_wave_ratio(self):
        cases=[
            {"pre_price":10, "open":10.5, "high":11, "low":9},
            {"pre_price":10, "open":7, "high":11, "low":9},
            {"pre_price":10, "open":12, "high":11, "low":9},
            {"pre_price":0, "open":10.5, "high":11, "low":9},
        ]

        for case in cases:
            try:
                dict = wv.calc_wave_ratio(case["pre_price"], case["open"], case["high"], case["low"])
                self.assertEqual(dict["min_ratio"], -0.15)
                self.assertEqual(dict["max_ratio"], 0.05)
            except ValueError as ve:
                print(ve.message, "Test ValueError OK!")
            except ZeroDivisionError as zde:
                print(zde.message, "Test ZeroDivisionError OK!")


    wave_ratio_df = pd.DataFrame(
                [
                    {"max_ratio":0.0001, "min_ratio":-0.0001},
                    {"max_ratio":0.0002, "min_ratio":-0.0002},
                    {"max_ratio":0.0003, "min_ratio":-0.0002},
                    {"max_ratio":0.0150, "min_ratio":-0.0150},
                ]
        )
    def test_calc_ratio_table_index_and_columns(self):
        dict = wv.calc_ratio_table_index_and_columns(max_ratio=0.02, min_ratio=-0.018)
        index, columns = dict["index"], dict["columns"]
        self.assertEqual(len(index), 180)
        self.assertEqual(len(columns), 200)
        self.assertEqual(index[1], "0.0001")
        self.assertEqual(columns[151], "0.0151")

        df = wv.calc_ratio_table(self.wave_ratio_df, index, columns)
        self.assertEqual(df["0.0000"]["0.0000"], 4)
        self.assertEqual(df["0.0001"]["0.0001"], 4)
        self.assertEqual(df["0.0002"]["0.0002"], 3)
        self.assertEqual(df["0.0002"]["0.0003"], 2)
        self.assertEqual(df["0.0140"]["0.0140"], 1)
        self.assertEqual(df["0.0190"]["0.0160"], 0)
        #print(df)
        df.to_csv("/home/chengang/Data/df.csv")

        table = wv.calc_length_ratio(df, 4)
        #self.assertEqual(table)


if __name__ == "__main__":
    unittest.main()
