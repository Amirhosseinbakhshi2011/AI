"""
کلاینت ارتباط با سرویس هوش مصنوعی (OpenAI و سازگاران).
مدیریت خطا، تایم‌اوت و قطع اینترنت در این لایه انجام می‌شود.
"""

from typing import Generator, List, Dict, Any
import openai
from openai import OpenAI, APITimeoutError, APIConnectionError, RateLimitError, AuthenticationError

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class AIClient:
    """کلاینت سطح پایین برای ارسال درخواست به مدل."""

    def __init__(self) -> None:
        client_kwargs: Dict[str, Any] = {
            "api_key": settings.openai_api_key,
            "timeout": settings.request_timeout,
        }
        if settings.openai_base_url:
            client_kwargs["base_url"] = settings.openai_base_url

        self.client = OpenAI(**client_kwargs)
        self.model = settings.openai_model

    def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
    ) -> str | Generator[str, None, None]:
        """
        ارسال پیام‌ها به مدل و دریافت پاسخ.

        Args:
            messages: لیست پیام‌ها با فرمت OpenAI
            stream: اگر True باشد، پاسخ به صورت جریانی برگردانده می‌شود

        Returns:
            رشته کامل پاسخ یا ژنراتور توکن‌ها
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                stream=stream,
            )

            if stream:
                return self._stream_response(response)
            else:
                content = response.choices[0].message.content or ""
                return content.strip()

        except AuthenticationError as e:
            logger.error(f"خطای احراز هویت: {e}")
            raise ValueError("کلید API نامعتبر است. لطفاً .env را بررسی کنید.") from e
        except RateLimitError as e:
            logger.error(f"محدودیت نرخ درخواست: {e}")
            raise RuntimeError("تعداد درخواست‌ها بیش از حد مجاز است. کمی صبر کنید.") from e
        except APITimeoutError as e:
            logger.error(f"تایم‌اوت: {e}")
            raise TimeoutError(
                f"درخواست بیش از {settings.request_timeout} ثانیه طول کشید. اتصال اینترنت را بررسی کنید."
            ) from e
        except APIConnectionError as e:
            logger.error(f"خطای اتصال: {e}")
            raise ConnectionError(
                "اتصال به سرور برقرار نشد. اینترنت خود را بررسی کنید یا بعداً تلاش نمایید."
            ) from e
        except Exception as e:
            logger.exception("خطای غیرمنتظره در ارتباط با API")
            raise RuntimeError(f"خطای غیرمنتظره: {str(e)}") from e

    def _stream_response(self, response) -> Generator[str, None, None]:
        """استخراج توکن‌ها از پاسخ جریانی."""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content