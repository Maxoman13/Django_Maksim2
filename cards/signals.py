from django.db.models.signals import post_save
from django.dispatch import receiver
import asyncio

from anki.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
from .models import Card
from .telegram_bot import send_telegram_message
import os


@receiver(post_save, sender=Card)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        message = f'Новая карточка: {instance.question} была добавлена.'
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))