#!/usr/bin/env python3
"""
نقطه ورود اصلی برنامه دستیار هوش مصنوعی.
"""

import sys
from pathlib import Path

# اطمینان از اینکه ریشه پروژه در sys.path باشد
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import settings
from utils.logger import get_logger
from ui.main_window import MainWindow

logger = get_logger("main")


def main() -> None:
    try:
        # اعتبارسنجی تنظیمات قبل از شروع UI
        settings.validate()
        logger.info("تنظیمات معتبر است. در حال راه‌اندازی رابط کاربری...")

        app = MainWindow()
        app.mainloop()

    except ValueError as e:
        # خطای تنظیمات (مثلاً نبود کلید API)
        print(f"\n[خطا] {e}\n")
        print("لطفاً فایل .env را بر اساس .env.example بسازید و کلید API را وارد کنید.")
        sys.exit(1)
    except Exception as e:
        logger.exception("خطای بحرانی در راه‌اندازی برنامه")
        print(f"\n[خطای بحرانی] {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()