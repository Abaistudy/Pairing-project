import fractions
import random

# 将带分数的字符串转换为 Fraction
import re


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
        numerator = random.randint(1, 9 * denominator - 1)
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

    subexpression = fraction_to_mixed(numbers[0])
    current_value = numbers[0]  # 追踪当前计算的值
    for i in range(1, num_count):
        op = random.choice(operators)

        # 确保除数不为0
        if op == '÷':
            while numbers[i] == 0:
                numbers[i] = generate_number(range_limit)
            current_value = current_value / numbers[i]

        # 确保减法不会产生负数，考虑前面的乘法或除法优先级
        elif op == '-':
            # 计算当前子表达式的值以避免负数
            right_value = eval_expression(fraction_to_mixed(numbers[i]))
            if current_value - right_value < 0:
                numbers[i] = generate_number(range_limit)  # 重新生成一个较小的右操作数
                right_value = eval_expression(fraction_to_mixed(numbers[i]))  # 更新右操作数的值
            current_value = current_value - right_value

        # 如果是乘法
        elif op == '*':
            current_value = current_value * numbers[i]

        # 如果是加法
        elif op == '+':
            current_value = current_value + numbers[i]

        # 拼接表达式
        subexpression += f" {op} {fraction_to_mixed(numbers[i])}"

    # 只有当子运算式包含两个或更多运算符时才加括号
    return f"({subexpression})" if num_count > 1 else subexpression


# 生成完整的运算表达式，由 2 个子运算式组成，确保不会产生负数
def generate_expression(range_limit):
    subexpression_count = 2
    subexpressions = [generate_subexpression(range_limit) for _ in range(subexpression_count)]
    operators = ['+', '-', '*', '÷']

    expression = subexpressions[0]
    current_value = eval_expression(subexpressions[0])  # 计算当前表达式的值
    for i in range(1, subexpression_count):
        op = random.choice(operators)

        next_value = eval_expression(subexpressions[i])

        # 初步确保减法不会导致负数，计算当前值并调整
        if op == '-':
            if current_value - next_value < 0:
                subexpressions[i] = generate_subexpression(range_limit)  # 调整右操作数
                next_value = eval_expression(subexpressions[i])  # 重新计算
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
