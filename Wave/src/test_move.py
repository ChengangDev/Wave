# -*- coding: utf-8 -*-
import unittest
import fetch as fch
import pvt
import pandas as pd
import move


class TestMV(unittest.TestCase):
    def test_mv(self):
        mv = move.MV(240, 240)
        for i in range(240):
            mv.push(i)
            self.assertEqual(mv.ma(1), i)
            self.assertEqual(mv.mmax(i+1), i)
            self.assertEqual(mv.mmin(i+1), 0)
            self.assertEqual(mv.mmax(1), i)
            self.assertEqual(mv.mmin(1), i)

        self.assertEqual(mv.ma(240), (0+239)/2.0)
        self.assertEqual(mv.ma(240)*240, mv.msum(240))

    def test_dist(self):
        cases = [
            ('9:30:00', 12.0),
            ('9:30:04', 14.0),
            ('9:31:00', 12.0),
            ('9:32:00', 11.0),
            ('9:32:04', 12.8),
            ('9:32:50', 12.2),
            ('9:33:00', 12.9),
            ('9:37:00', 12.9),
            ('9:38:00', 12.9),
        ]

        red = [
            None,
            None,
            13.0,
            12.0,
            None,
            None,
            12.0,
            12.9,
            12.9,
            None
        ]

        dist = move.Dist()
        for i in range(len(cases)):
            t = cases[i]
            out = dist.reduce(t[0], t[1])
            self.assertEqual(out, red[i])


if __name__ == "__main__":
    unittest.main()