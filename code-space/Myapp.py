import re
import fractions
import random
import argparse


# 将带分数的字符串转换为 Fraction
def mixed_to_fraction(mixed_str):
    if "'" in mixed_str:
        whole, frac = mixed_str.split("'")
        whole = int(whole)
        numerator, denominator = map(int, frac.split('/'))
        return fractions.Fraction(whole * denominator + numerator, denominator)
    elif "/" in mixed_str:
        numerator, denominator = map(int, mixed_str.split('/'))
        return fractions.Fraction(numerator, denominator)
    else:
        return fractions.Fraction(int(mixed_str), 1)


# 将分数转换为带分数的字符串
def fraction_to_mixed(f):
    if f.denominator == 1:
        return str(f.numerator)
    elif f.numerator > f.denominator:
        whole = f.numerator // f.denominator
        remainder = f.numerator % f.denominator
        return f"{whole}'{remainder}/{f.denominator}" if remainder != 0 else str(whole)
    return str(f)


# 生成随机自然数或真分数，避免分母为0的情况
def generate_number(range_limit):
    if random.choice([True, False]):
        # 生成自然数数
        return random.randint(1, range_limit - 1)
    else:
        # 生成真分数
        denominator = random.randint(2, range_limit - 1)  # 确保分母不为1或0
        numerator = random.randint(1, 10 * denominator - 1)
        while numerator % denominator == 0:
            numerator = random.randint(1, 9 * denominator - 1)
        return fractions.Fraction(numerator, denominator)


def eval_expression(expr):
    # 替换带分数为正确的 Fraction 表示
    expr = re.sub(r"(\d+)'(\d+)/(\d+)", lambda m: str(mixed_to_fraction(m.group(0))), expr)

    # 将分数转换为 Fraction 对象
    expr = re.sub(r"(\d+)/(\d+)", lambda m: str(fractions.Fraction(int(m.group(1)), int(m.group(2)))), expr)

    # 将 ÷ 替换为 /，使用 Fraction 处理除法
    expr = expr.replace('÷', '/')

    try:
        # 使用 eval 计算表达式，确保使用 fractions.Fraction 进行计算，避免浮点精度问题
        return eval(expr, {"__builtins__": None}, {"Fraction": fractions.Fraction})
    except ZeroDivisionError:
        return float('inf')  # 返回一个特殊值，表示出现了除以0的情况


# 生成子运算式，包含 1 到 3 个运算数，避免负数，考虑优先级
def generate_subexpression(range_limit):
    num_count = random.randint(1, 3)  # 随机生成1到3个运算数
    numbers = [generate_number(range_limit) for _ in range(num_count)]
    operators = ['+', '-', '*', '÷']

    # 当产生的单运算数是分数时，加上括号，避免出错
    if num_count == 1:
        if numbers[0].denominator == 1:
            return fraction_to_mixed(numbers[0])  # 如果只有一个运算数，不需要括号
        else:
            return f"({fraction_to_mixed(numbers[0])})"

    subexpression = fraction_to_mixed(numbers[0])
    for i in range(1, num_count):
        op = random.choice(operators)

        # 避免除0
        if op == '÷' and numbers[i] == 0:
            numbers[i] = generate_number(range_limit)

        # 避免出现负数，出现时转换为加法
        if op == '-' and numbers[i] > numbers[i - 1]:
            op = '+'

        subexpression += f" {op} {fraction_to_mixed(numbers[i])}"

        # 如果有多个运算数，加上括号
    return f"({subexpression})" if num_count > 1 else subexpression


# 生成完整的运算表达式，由 2 个子运算式组成，确保不会产生负数
def generate_expression(range_limit):
    subexpression_count = 2
    subexpressions = [generate_subexpression(range_limit) for _ in range(subexpression_count)]
    operators = ['+', '-', '*', '÷']

    # 避免最终表达式出现四个运算符
    matches = []
    for ch in subexpressions:
        if ch in operators:
            matches = matches.append(ch)

    expression = subexpressions[0]
    current_value = eval_expression(subexpressions[0])  # 计算当前表达式的值
    for i in range(1, subexpression_count):
        op = random.choice(operators)
        # 记录
        while len(matches) > 2 & (op not in matches):
            op = random.choice(operators)
        if op not in matches:
            matches.append(op)

        next_value = eval_expression(subexpressions[i])

        # 确保不会产生负数，出现时转换为加法
        if op == '-':
            if current_value - next_value < 0:
                op = '+'
                current_value = current_value + next_value
            else:
                current_value = current_value - next_value

        # 其他操作更新当前值
        elif op == '+':
            current_value = current_value + next_value
        elif op == '*':
            current_value = current_value * next_value
        elif op == '÷':
            while next_value == 0:
                subexpressions[i] = generate_subexpression(range_limit)  # 确保不除以0
                next_value = eval_expression(subexpressions[i])
            current_value = current_value / next_value

        # 拼接表达式
        expression += f" {op} {subexpressions[i]}"

    return expression, current_value


# 生成题目和答案
def generate_quiz(num_questions, range_limit):
    exercises = []
    answers = []

    for _ in range(num_questions):
        expression, answer = generate_expression(range_limit)
        while answer < 0:
            expression, answer = generate_expression(range_limit)
        exercises.append(expression)
        answers.append(fraction_to_mixed(fractions.Fraction(answer).limit_denominator()))

    with open("Exercises.txt", "w") as ex_file, open("Answers.txt", "w") as ans_file:
        for i, (exercise, answer) in enumerate(zip(exercises, answers), 1):
            ex_file.write(f"{i}. {exercise} = \n")
            ans_file.write(f"{i}. {answer}\n")


def grade(exercise_file, answer_file):
    with open(exercise_file, "r") as ex_file, open(answer_file, "r") as ans_file:
        exercises = ex_file.readlines()
        answers = ans_file.readlines()

    correct = []
    wrong = []

    for i, (exercise, answer) in enumerate(zip(exercises, answers), 1):
        # 去除题目中的编号，获取表达式部分
        expr = exercise.split('=')[0].strip()  # 去除 = 号后面的内容
        expr = re.sub(r'^\d+\.\s*', '', expr)  # 去除题目编号 "1. " 等格式

        # 将预期答案转换为标准 Fraction 形式
        expected_answer = answer.split('.')[1].strip()
        expected_fraction = mixed_to_fraction(expected_answer)

        # 计算表达式的答案
        calculated_fraction = fractions.Fraction(eval_expression(expr.replace('÷', '/'))).limit_denominator()

        # 比较计算结果和预期答案，统一比较 Fraction 对象而不是字符串
        if expected_fraction == calculated_fraction:
            correct.append(i)
        else:
            wrong.append(i)

    with open("Grade.txt", "w") as grade_file:
        grade_file.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        grade_file.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


# 主函数
def main():
    parser = argparse.ArgumentParser(description="四则运算题目生成器")

    parser.add_argument("-n", type=int, help="生成题目的个数")
    parser.add_argument("-r", type=int, help="题目中数值范围")
    parser.add_argument("-e", type=str, help="题目文件路径")
    parser.add_argument("-a", type=str, help="答案文件路径")

    args = parser.parse_args()

    if args.n and args.r:
        generate_quiz(args.n, args.r)
    elif args.e and args.a:
        grade(args.e, args.a)
    else:
        print("参数错误，请使用 -h 查看帮助信息")
        exit(1)


if __name__ == "__main__":
    main()
