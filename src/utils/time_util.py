from datetime import datetime
import pytz


def convert(time_str: str):
    """将UTC字符串时间转换为上海的字符串

    Args:
        time (str): 时间字符串(UTC)

    Returns:
        int: 时间戳
    """
    # 创建时间对象
    time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # 设置 UTC 时区
    utc_timezone = pytz.timezone("UTC")
    time = utc_timezone.localize(time)

    # 转换为上海时区
    shanghai_timezone = pytz.timezone("Asia/Shanghai")
    shanghai_time = time.astimezone(shanghai_timezone)

    # 转为字符串
    return shanghai_time.strftime("%Y-%m-%d %H:%M:%S")


def convert2datetime(time_str: str):
    """将上海的字符串转换为datetime对象

    Args:
        time_str (str): 时间字符串(上海时间)
    """
    # 创建时间对象
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    convert_res = convert("2021-08-28T14:00:00.000Z")
    res = convert2datetime(convert_res)
