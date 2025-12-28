"""
เขียนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""
import unittest


class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        if (number < 0):
            return "number can not be negative"
        divider = 5
        tailing_zeros = 0
        while (int(number / divider)):
            tailing_zeros += int(number / divider)
            divider *= 5
        return tailing_zeros
    
class TestSolution(unittest.TestCase):
    def setUp(self):
        # Create object before each test
        self.solution = Solution()
        
    def test_find_tailing_zeroes(self):
        test_cases = [
            (0, 0),
            (-4, "number can not be negative"),
            (8, 1)
        ]
        for input, expected in test_cases:
            with self.subTest(input=input):
                result = self.solution.find_tailing_zeroes(input)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()