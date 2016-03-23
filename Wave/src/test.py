# -*- coding: utf-8 -*-
import unittest
import wave as wv



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

if __name__ == "__main__":
    unittest.main()
