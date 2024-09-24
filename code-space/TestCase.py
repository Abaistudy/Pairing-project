import unittest
import fractions
import sys
from Myapp import (
    mixed_to_fraction,
    fraction_to_mixed,
    generate_number,
    generate_subexpression,
    eval_expression,
    generate_expression,
    generate_quiz,
    grade,
    main
)


class TestMathOperations(unittest.TestCase):

    # 测试混合分数转换
    def test_mixed_to_fraction(self):
        self.assertEqual(mixed_to_fraction("2'3/4"), fractions.Fraction(11, 4))
        self.assertEqual(mixed_to_fraction("3/5"), fractions.Fraction(3, 5))
        self.assertEqual(mixed_to_fraction("5"), fractions.Fraction(5, 1))

    # 测试分数转换为混合分数字符串
    def test_fraction_to_mixed(self):
        self.assertEqual(fraction_to_mixed(fractions.Fraction(11, 4)), "2'3/4")
        self.assertEqual(fraction_to_mixed(fractions.Fraction(3, 5)), "3/5")
        self.assertEqual(fraction_to_mixed(fractions.Fraction(5, 1)), "5")

    # 测试减法不出现负数
    def test_no_negative_subtraction(self):
        for _ in range(100):  # 多次测试
            result = generate_subexpression(10)
            if '-' in result:
                # 检查是否产生负数
                eval_result = eval_expression(result.replace('÷', '/'))
                self.assertTrue(eval_result >= 0, "表达式不应生成负数")

    # 测试避免除以0
    def test_avoid_zero_division(self):
        for _ in range(100):  # 多次测试
            result = generate_subexpression(10)
            self.assertNotIn("0", result)  # 确保没有0作为除数

    # 测试表达式求值
    def test_eval_expression(self):
        self.assertEqual(fractions.Fraction(eval_expression("(2'1/3 + 3/4)")).limit_denominator(),
                         fractions.Fraction(37, 12))

    # 测试生成完整运算表达式
    def test_generate_expression(self):
        expression, answer = generate_expression(10)
        self.assertTrue(isinstance(expression, str))
        self.assertTrue(eval_expression(expression) >= 0)

    # 测试生成题目到文件
    def test_generate_quiz(self):
        generate_quiz(5, 10)
        with open("Exercises.txt", "r") as ex_file:
            exercises = ex_file.readlines()
        with open("Answers.txt", "r") as ans_file:
            answers = ans_file.readlines()
        self.assertEqual(len(exercises), 5)
        self.assertEqual(len(answers), 5)

    # 测试批改功能
    def test_grade(self):
        generate_quiz(5, 10)
        generate_quiz(5, 10)  # 生成一套题目以进行批改
        grade("Exercises.txt", "Answers.txt")
        with open("Grade.txt", "r") as grade_file:
            results = grade_file.read()
        self.assertIn("Correct:", results)
        self.assertIn("Wrong:", results)

    # 测试命令行参数处理错误情况
    def test_main_args_error(self):
        # 使用 mock 来测试错误情况
        with self.assertRaises(SystemExit):
            sys.argv = ["script_name"]
            main()

    # 测试边界条件
    def test_generate_number_boundary(self):
        for _ in range(100):
            num = generate_number(1000)
            self.assertNotEqual(num.denominator, 0)


if __name__ == "__main__":
    unittest.main()
