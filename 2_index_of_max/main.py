"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


import unittest


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        if len(numbers) <= 0:
            return "list can not blank"
        temp = {"index": 0, "value": 0}
        for index in range(len(numbers)):
            if numbers[index] > temp["value"]:
                temp["value"] = numbers[index]
                temp["index"] = index
        return temp["index"]

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()
        
    def test_find_tailing_zeroes(self):
        test_cases = [
            ([0], 0),
            ([-4, 10, 11, 500], 3),
            ([1,2,3,4,5,6,7], 6),
            ([1025, 500, -722 , -52, 5 ,10], 0),
            (["string", 5, 100, 89], 0)
        ]
        
        for input, expected in test_cases:
            with self.subTest(input=input):
                result = self.solution.find_max_index(input)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()