import fractions
import random


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
        numerator = random.randint(1, 9 * denominator - 1)
        while numerator % denominator == 0:
            numerator = random.randint(1, 9 * denominator - 1)
        return fractions.Fraction(numerator, denominator)
