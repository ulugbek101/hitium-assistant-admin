import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Task
from api.telegram import send_message

logger = logging.getLogger('task_logger')

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New task created: {instance.name}")
    else:
        for brigade in instance.brigades.all():
            foreman = brigade.foreman
            workers = brigade.workers.all()

            try:
                send_message(chat_id=foreman.telegram_id, text="Бригадир, к вам поступила новая задача")
                logger.info(f"Message sent to foreman {foreman.first_name} {foreman.last_name}")
            except Exception as e:
                logger.error(f"Error sending message to foreman {foreman.first_name} {foreman.last_name}: {e}")

            for worker in workers:
                try:
                    send_message(chat_id=worker.telegram_id, text="Работник, к вам поступила новая задача")
                    logger.info(f"Message sent to worker {worker.first_name} {worker.last_name}")
                except Exception as e:
                    logger.error(f"Error sending message to worker {worker.first_name} {worker.last_name}: {e}")
