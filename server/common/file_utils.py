def bytes_to_mb(bytes_value):
    """
    将字节数转换为兆字节（MB）。

    :param bytes_value: 要转换的字节数
    :return: 转换后的兆字节数
    """
    # 1 MB = 1024 * 1024 字节
    mb_value = bytes_value / (1024 * 1024)
    return mb_value