"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""
from typing import Tuple
import unittest


class Solution:
    THAI_REFERENCE = {
        0: "ศูนย์",
        1: "หนึ่ง",
        2: "สอง",
        3: "สาม",
        4: "สี่",
        5: "ห้า",
        6: "หก",
        7: "เจ็ด",
        8: "แปด",
        9: "เก้า",

    }

    THAI_DIGIT_REF = {
        2: "สิบ",
        3: "ร้อย",
        4: "พัน",
        5: "หมื่น",
        6: "แสน",
        7: "ล้าน",
    }

    TWO_DIGIT_REF = {
        1: "เอ็ด",
        2: "ยี่"
    }

    divider = 10

    def find_key_by_value(self, dict: dict[int, str], value: str) -> int | None:
        for key, val in dict.items():
            if val == value:
                return key
        return None

    def compare_digit_value(self, dict: dict[int, str], pre_value: str, value: str) -> bool:
        pre_digit = self.find_key_by_value(dict, pre_value)
        current_digit = self.find_key_by_value(dict, value)
        if (pre_digit is None or current_digit is None):
            return False
        return pre_digit > current_digit

    def read_two_digit(self, digit: int, number: int) -> str | None:
        if (digit % 6 == 2):
            if (digit == 2 and number == 2):
                return self.TWO_DIGIT_REF[2]
            if (int(number / self.divider) > 2):
                return self.THAI_REFERENCE[int(number / self.divider)]
        return None if number == 0 and digit > 1 else self.THAI_REFERENCE[number]

    def read_last_digit(self, number_str: int, word: str, number: int) -> str:
        if number_str > 0 and word == self.THAI_DIGIT_REF[2] and number == 1:
            return self.TWO_DIGIT_REF[1]
        return self.THAI_REFERENCE[number]

    def read_thai_digit(self, digit: int) -> str | None:
        find_digit = self.THAI_DIGIT_REF.get(digit)
        if (find_digit is None):
            ref = digit % 6
            return self.THAI_DIGIT_REF[ref] if self.THAI_DIGIT_REF.get(ref) else None
        return find_digit

    def number_to_thai(self, number: int) -> list[str] | str:
        if (number < 0):
            return "number can not less than 0"
        if (number > 10000000):
            return "number can not more than 10000000"

        number_str = str(number)
        digit = len(number_str)
        i = 0
        convert_to_thai = []
        while (digit > 0):
            number_at_position = int(number_str[i])
            number_at_digit = self.read_thai_digit(digit)
            if (self.read_two_digit(digit, number_at_position) is not None and i < len(number_str) - 1):
                convert_to_thai.append(
                    self.read_two_digit(digit, number_at_position))
            if number_at_digit is not None and i < len(number_str) - 1:
                convert_to_thai.append(number_at_digit)
            elif len(convert_to_thai) > 1:
                convert_to_thai.append(
                    self.read_last_digit(int(number_str[i - 1]), convert_to_thai[-1], number_at_position))
            else:
                convert_to_thai += self.THAI_REFERENCE[number_at_position]
            i += 1
            digit -= 1

        convert_to_string = ""
        remove_index = []
        for i in range(len(convert_to_thai)):
            if (i > 0 and convert_to_thai[i - 1] == self.THAI_REFERENCE[1] and convert_to_thai[i] == self.THAI_DIGIT_REF[2]):
                remove_index.append(i - 1)
            if (i != 0 and i == len(convert_to_thai) - 1 and convert_to_thai[i] == self.THAI_REFERENCE[0]):
                remove_index.append(i)
            if (i > 0 and self.compare_digit_value(self.THAI_DIGIT_REF, convert_to_thai[i - 1], convert_to_thai[i])):
                remove_index.append(i)

        for i in range(len(convert_to_thai)):
            if (i in remove_index):
                continue
            convert_to_string += convert_to_thai[i]
        return convert_to_string


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_number_to_thai(self):
        test_cases = [
            (0, "ศูนย์"),
            (1, "หนึ่ง"),
            (10, "สิบ"),
            (100, "หนึ่งร้อย"),
            (1000, "หนึ่งพัน"),
            (10000000, "สิบล้าน"),
            (11, "สิบเอ็ด"),
            (13, "สิบสาม"),
            (20, "ยี่สิบ"),
            (54, "ห้าสิบสี่"),
            (99, "เก้าสิบเก้า"),
            (101, "หนึ่งร้อยหนึ่ง"),
            (120, "หนึ่งร้อยยี่สิบ"),
            (121, "หนึ่งร้อยยี่สิบเอ็ด"),
            (123, "หนึ่งร้อยยี่สิบสาม"),
            (110, "หนึ่งร้อยสิบ"),
            (111, "หนึ่งร้อยสิบเอ็ด"),
            (3345, "สามพันสามร้อยสี่สิบห้า"),
            (43219, "สี่หมื่นสามพันสองร้อยสิบเก้า")
        ]

        for input, expected in test_cases:
            with self.subTest(input=input):
                result = self.solution.number_to_thai(input)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
    # solution = Solution()
    # test_cases = [
    #     (11, "สิบเอ็ด"),
    #     (101, "หนึ่งร้อยหนึ่ง"),
    # ]
    # for input, expected in test_cases:
    #     result = solution.number_to_thai(input)
    #     print(result)
