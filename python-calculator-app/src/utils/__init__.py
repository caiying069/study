# 验证输入的值是否为有效的数字
# 参数:
#   value (Any): 待验证的值，可以是任意类型
# 返回:
#   bool: 如果值能转换为浮点数则返回 True，否则返回 False
def validate_number(value):
    try:
        # 尝试将输入的值转换为浮点数
        float(value)
        # 转换成功，说明输入是有效的数字，返回 True
        return True
    except (ValueError, TypeError):
        # 转换失败，捕获 ValueError 或 TypeError 异常，返回 False
        return False


# 将计算结果格式化为特定字符串
# 参数:
#   result (Any): 待格式化的计算结果，可以是任意类型
# 返回:
#   str: 格式化后的字符串，格式为 "计算结果是: {result}"
def format_result(result):
    return f"The result is: {result}"