from typing import Literal


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class APIStatusError(Exception):
    """API状态错误的基类。"""
    status_code: int


class RateLimitError(APIStatusError):
    """特定于HTTP 429错误的异常类。"""
    status_code: Literal[429] = 429
