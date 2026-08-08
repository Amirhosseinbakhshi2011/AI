"""
مدیریت تاریخچه گفتگوها.
هر گفتگو در یک فایل JSON جداگانه ذخیره می‌شود تا قابل بازیابی و پشتیبان‌گیری باشد.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ChatHistory:
    """مدیریت ذخیره‌سازی و بازیابی تاریخچه گفتگو."""

    def __init__(self) -> None:
        self.chats_dir = settings.chats_dir
        self.current_chat_id: Optional[str] = None
        self.messages: List[Dict[str, str]] = []

    def new_chat(self) -> str:
        """ایجاد یک گفتگوی جدید و برگرداندن شناسه آن."""
        self.current_chat_id = str(uuid.uuid4())
        self.messages = []
        logger.info(f"گفتگوی جدید ایجاد شد: {self.current_chat_id}")
        return self.current_chat_id

    def add_message(self, role: str, content: str) -> None:
        """افزودن یک پیام به تاریخچه فعلی."""
        if role not in ("system", "user", "assistant"):
            raise ValueError(f"نقش نامعتبر: {role}")
        self.messages.append({"role": role, "content": content})
        self._save()

    def get_messages(self) -> List[Dict[str, str]]:
        """برگرداندن کپی از پیام‌های فعلی."""
        return list(self.messages)

    def load_chat(self, chat_id: str) -> bool:
        """بارگذاری یک گفتگو از فایل. در صورت موفقیت True برمی‌گرداند."""
        file_path = self.chats_dir / f"{chat_id}.json"
        if not file_path.exists():
            logger.warning(f"فایل گفتگو یافت نشد: {chat_id}")
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.current_chat_id = chat_id
            self.messages = data.get("messages", [])
            logger.info(f"گفتگو بارگذاری شد: {chat_id}")
            return True
        except Exception as e:
            logger.error(f"خطا در بارگذاری گفتگو {chat_id}: {e}")
            return False

    def list_chats(self) -> List[Dict[str, str]]:
        """لیست تمام گفتگوهای موجود با عنوان و تاریخ."""
        chats = []
        for file_path in sorted(self.chats_dir.glob("*.json"), reverse=True):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                chats.append({
                    "id": file_path.stem,
                    "title": data.get("title", "بدون عنوان"),
                    "created_at": data.get("created_at", ""),
                    "updated_at": data.get("updated_at", ""),
                })
            except Exception:
                continue
        return chats

    def delete_chat(self, chat_id: str) -> bool:
        """حذف یک گفتگو."""
        file_path = self.chats_dir / f"{chat_id}.json"
        if file_path.exists():
            file_path.unlink()
            if self.current_chat_id == chat_id:
                self.new_chat()
            return True
        return False

    def _save(self) -> None:
        """ذخیره گفتگوی فعلی روی دیسک."""
        if not self.current_chat_id:
            self.new_chat()

        # عنوان ساده بر اساس اولین پیام کاربر
        title = "گفتگوی جدید"
        for msg in self.messages:
            if msg["role"] == "user":
                title = msg["content"][:50].strip()
                if len(msg["content"]) > 50:
                    title += "..."
                break

        now = datetime.now().isoformat(timespec="seconds")
        data = {
            "id": self.current_chat_id,
            "title": title,
            "created_at": now if not self.messages else self._get_created_at(),
            "updated_at": now,
            "messages": self.messages,
        }

        file_path = self.chats_dir / f"{self.current_chat_id}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطا در ذخیره گفتگو: {e}")

    def _get_created_at(self) -> str:
        """خواندن تاریخ ایجاد از فایل موجود در صورت وجود."""
        file_path = self.chats_dir / f"{self.current_chat_id}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("created_at", datetime.now().isoformat(timespec="seconds"))
            except Exception:
                pass
        return datetime.now().isoformat(timespec="seconds")