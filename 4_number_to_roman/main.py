"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""

import unittest


class Solution:
    ROMAN_REFERENCE = {
        1000000000: "M\u033f",
        900000000: "C\u033f(M\u033f)",
        500000000: "D\u033f",
        400000000: "C\u033f(D\u033f)",
        100000000: "C\u033f",
        90000000: "X\u033f(C\u033f)",
        50000000: "L\u033f",
        40000000: "X\u033f(L\u033f)",
        10000000: "X\u033f",
        9000000: "I\u033f(X\u033f)",
        5000000: "V\u033f",
        4000000: "I\u033f(V\u033f)",
        1000000: "M\u0305",
        900000: "C\u0305M\u0305",
        500000: "D\u0305",
        400000: "C\u0305D\u0305",
        100000: "C\u0305",
        90000: "X\u0305C\u0305",
        50000: "L\u0305",
        40000: "X\u0305L\u0305",
        10000: "X\u0305",
        9000: "I\u0305X\u0305",
        5000: "V\u0305",
        4000: "I\u0305V\u0305",
        1000: "M",
        900: "CM",
        500: "D",
        400: "CD",
        100: "C",
        90: "XC",
        50: "L",
        40: "XL",
        10: "X",
        9: "IX",
        5: "V",
        4: "IV",
        1: "I",
    }

    def number_to_roman(self, number: int) -> str:
        if not (0 < number < 4000000000):
            return "Number out of range (1 - 3,999,999,999)"

        result = ""

        for value in self.ROMAN_REFERENCE:
            while number >= value:
                result += self.ROMAN_REFERENCE[value]
                number -= value

        return result


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()
        
    def test_number_to_roman(self):
        test_cases = [
            # Standard
            (1, "I"),
            (4, "IV"),
            (9, "IX"),
            (58, "LVIII"),
            (1994, "MCMXCIV"),
            (3999, "MMMCMXCIX"),
            # Single Vinculum (x1,000)
            (4000, "I\u0305V\u0305"),
            (5000, "V\u0305"),
            (10600, "X\u0305DC"),
            # Double Vinculum (x1,000,000)
            (1000000, "M\u0305"),
            (5000000, "V\u033f"),
            (3000000000, "M\u033fM\u033fM\u033f"),
            # Out of Range
            (0, "Number out of range (1 - 3,999,999,999)"),
            (4000000000, "Number out of range (1 - 3,999,999,999)"),
        ]

        for input_val, expected_output in test_cases:
            with self.subTest(input_val=input_val):
                self.assertEqual(self.solution.number_to_roman(input_val), expected_output)


if __name__ == "__main__":
    unittest.main()
