# -*- coding: utf-8 -*-
import unittest
import wave as wv

if __name__ == "__main__":
    unittest.main()

class TestWave(unittest.TestCase):

    def test_calc_wave_ratio(self):
        cases=[
            {"pre_prece":10, "open":10.5, "high":11, "low":9}
        ]

        for case in cases:
            dict = wv.calc_wave_ratio(case["pre_price"], case["open"], case["high"], case["low"])
            self.assertEqual(dict["min_ratio"], -0.15)
            self.assertEqual(dict["max_ratio"], 0.05)
