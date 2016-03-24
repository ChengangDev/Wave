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
                print(ve.message)
            except ZeroDivisionError as zde:
                print(zde.message)


    def test_calc_ratio_table(self):
        wave_ratio_df = pd.DataFrame(
                [
                    {"max_ratio":0.01, "min_ratio":-0.01},
                    {"max_ratio":0.011, "min_ratio":-0.011},
                    {"max_ratio":0.001, "min_ratio":-0.011},
                    {"max_ratio":0.015, "min_ratio":-0.015},
                ]
        )

        df = wv.calc_ratio_table(wave_ratio_df, max_ratio=0.02, min_ratio=-0.02)
        self.assertEqual(df["0.0000"]["0.0000"], 4)
        df.to_csv("/home/chengang/Data/test.csv")

if __name__ == "__main__":
    unittest.main()
