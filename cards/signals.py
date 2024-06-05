from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Card
from .telegram_bot import send_telegram_message
import os


@receiver(post_save, sender=Card)
async def notify_admin(sender, instance, created, **kwargs):
    if created:
        message = f'Новая карточка: {instance.title} была добавлена.'
        await send_telegram_message(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("YOUR_PERSONAL_CHAT_ID"), message,
                                    parse_mode="HTML")
