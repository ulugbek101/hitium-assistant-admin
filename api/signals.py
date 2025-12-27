import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from api.models import Task
from api.telegram import send_message
from api.translations import build_task_message

logger = logging.getLogger('task_logger')

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New task created: {instance.name}")

    else:
        for brigade in instance.brigades.all():
            foreman = brigade.foreman
            workers = brigade.workers.all()

            title = instance.name
            description = instance.description if len(instance.description) <= 100 else f"{instance.description[:100]} ..."
            deadline = instance.deadline.strftime("%d-%m-%Y")

            text = build_task_message(lang=foreman.lang, title=title, description=description, deadline=deadline)

            try:
                send_message(chat_id=foreman.telegram_id, text=text)
                logger.info(f"Message sent to foreman {foreman.first_name} {foreman.last_name}")
            except Exception as e:
                logger.error(f"Error sending message to foreman {foreman.first_name} {foreman.last_name}: {e}")

            for worker in workers:
                text = build_task_message(lang=worker.lang, title=title, description=description, deadline=deadline)
                try:
                    send_message(chat_id=worker.telegram_id, text=text)
                    logger.info(f"Message sent to worker {worker.first_name} {worker.last_name}")
                except Exception as e:
                    logger.error(f"Error sending message to worker {worker.first_name} {worker.last_name}: {e}")
