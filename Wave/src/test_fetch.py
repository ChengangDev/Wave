# -*- coding: utf-8 -*-
import unittest
import fetch as fch
import pandas as pd


class TestFetch(unittest.TestCase):
    def test_export_ratio_table(self):
        df = fch.export_ratio_table('600848', '20150105', '20150109', 'one')
        self.assertEqual(df.iloc[0, 0], 5)
        self.assertEqual(df.iloc[88, 0], 4)
        self.assertEqual(df.iloc[0, 1], 1)
        self.assertEqual(df.iloc[88, 1], 0.8)
        # print(df)



if __name__ == "__main__":
    unittest.main()
