"""Генерация уникальных id (hex)."""

import time
import random


def generate_id():
    return f"{int(time.time() * 1000):x}{random.randint(0, 0xFFFFFF):x}"
