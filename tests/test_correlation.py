import unittest

from correlation import from_csv, interpret, pearson, spearman


class TestPearson(unittest.TestCase):
    def test_perfect_positive(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.assertAlmostEqual(pearson(x, y), 1.0, places=4)

    def test_perfect_negative(self):
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]
        self.assertAlmostEqual(pearson(x, y), -1.0, places=4)

    def test_zero_variance(self):
        self.assertEqual(pearson([1, 1, 1], [1, 2, 3]), 0.0)

    def test_known_value(self):
        # 教科书示例：x=[1,2,3], y=[1,2,3] -> 1；弱相关约 0.9
        x = [1, 2, 3, 4]
        y = [1, 2, 3, 5]
        r = pearson(x, y)
        self.assertGreater(r, 0.9)


class TestSpearman(unittest.TestCase):
    def test_monotonic(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 100]  # 单调
        self.assertAlmostEqual(spearman(x, y), 1.0, places=4)

    def test_ties(self):
        x = [1, 2, 2, 3]
        y = [2, 1, 1, 0]
        rho = spearman(x, y)
        self.assertLess(rho, -0.5)


class TestInterpret(unittest.TestCase):
    def test_labels(self):
        self.assertIn("强相关", interpret(0.95))
        self.assertIn("负", interpret(-0.8))
        self.assertIn("无相关", interpret(0.02))


class TestCSV(unittest.TestCase):
    def test_read_csv(self):
        csv = "hours,score\n1,2\n2,4\n3,6\n"
        xs, ys = from_csv(csv)
        self.assertEqual(xs, [1.0, 2.0, 3.0])
        self.assertEqual(ys, [2.0, 4.0, 6.0])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            pearson([1, 2], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
