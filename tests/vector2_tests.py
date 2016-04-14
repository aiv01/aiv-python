import unittest
from aiv.math.vector2 import Vector2

class TestVector2(unittest.TestCase):

    def test_sum_with_vector3(self):
        v0 = Vector2(17, 30)
        v1 = Vector2(22, 17)
        v_sum = v0 + v1
        self.assertEqual(v_sum, Vector2(39, 47))

    def test_sub_with_vector3(self):
        v0 = Vector2(17, 30)
        v1 = Vector2(5, 5)
        v_sub = v0 - v1
        self.assertEqual(v_sub, Vector2(12, 25))

    def test_sum_with_num(self):
        v0 = Vector2(17, 30)
        v_sum = v0 + 5
        self.assertEqual(v_sum, Vector2(22, 35))

    def test_mul_with_vector3(self):
        v0 = Vector2(17, 30)
        v1 = Vector2(1, 1)
        v_mul = v0 * v1
        self.assertEqual(v_mul, Vector2(17, 30))
        self.assertEqual(v_mul * Vector2(2, 2), Vector2(34, 60))

    def test_mul_with_num(self):
        v0 = Vector2(17, 30)
        v_mul = v0 * 1
        self.assertEqual(v_mul, Vector2(17, 30))
        self.assertEqual(v_mul * Vector2(2, 2), Vector2(34, 60))

    def test_indexing(self):
        v = Vector2(17, 30)
        self.assertEqual(v[0], 17)
        self.assertEqual(v[1], 30)

    def test_normalized(self):
        v0 = Vector2(1, 0)
        self.assertEqual(v0.normalized, Vector2(1, 0))
        v1 = Vector2(2, 0)
        self.assertEqual(v1.normalized, Vector2(1, 0))

if __name__ == '__main__':
   unittest.main()
