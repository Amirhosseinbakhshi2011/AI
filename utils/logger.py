"""
سیستم لاگ‌گیری ساده و یکپارچه برای کل پروژه.
"""

import logging
import sys
from pathlib import Path

from config.settings import BASE_DIR


def get_logger(name: str) -> logging.Logger:
    """ایجاد و پیکربندی لاگر."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # فرمت استاندارد
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # خروجی کنسول
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # فایل لاگ (اختیاری)
        log_dir = BASE_DIR / "logs"
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "assistant.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger