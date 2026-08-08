"""
ماژول تنظیمات پروژه.
تنظیمات از فایل .env بارگذاری می‌شوند و اعتبارسنجی می‌گردند.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# مسیر ریشه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# بارگذاری .env
load_dotenv(BASE_DIR / ".env")


class Settings:
    """کلاس مرکزی تنظیمات برنامه."""

    def __init__(self) -> None:
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
        self.openai_base_url: str | None = os.getenv("OPENAI_BASE_URL") or None
        if self.openai_base_url:
            self.openai_base_url = self.openai_base_url.strip()

        self.request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
        self.max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
        self.default_language: str = os.getenv("DEFAULT_LANGUAGE", "fa").strip().lower()

        # مسیرهای داده
        self.data_dir: Path = BASE_DIR / "data"
        self.chats_dir: Path = self.data_dir / "chats"
        self.chats_dir.mkdir(parents=True, exist_ok=True)

    def validate(self) -> None:
        """بررسی وجود کلید API و مقادیر منطقی."""
        if not self.openai_api_key:
            raise ValueError(
                "کلید API یافت نشد. لطفاً فایل .env را بر اساس .env.example ایجاد کنید "
                "و OPENAI_API_KEY را تنظیم نمایید."
            )
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("TEMPERATURE باید بین ۰ تا ۲ باشد.")
        if self.request_timeout < 5:
            raise ValueError("REQUEST_TIMEOUT نباید کمتر از ۵ ثانیه باشد.")


# نمونه سراسری
settings = Settings()