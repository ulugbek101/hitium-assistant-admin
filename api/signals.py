import logging

from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from api.models import Task, BotUser, Worker, User
from api.telegram import send_message
from api.translations import build_task_message

logger = logging.getLogger('task_logger')


@receiver(m2m_changed, sender=Task.brigades.through)
def task_brigades_changed(sender, instance, action, pk_set, **kwargs):
    """
    Send messages when brigades are assigned to a Task.
    """
    if action == "post_add":
        brigades = instance.brigades.filter(pk__in=pk_set)

        for brigade in brigades:
            # Foreman
            foreman = brigade.foreman
            try:
                lang = BotUser.objects.get(telegram_id=foreman.telegram_id).lang
                text = build_task_message(
                    lang=lang,
                    title=instance.name,
                    description=(instance.description[:100] + "..." if len(instance.description) > 100 else instance.description),
                    deadline=instance.deadline.strftime("%d-%m-%Y")
                )
                send_message(chat_id=foreman.telegram_id, text=text)
                logger.info(f"Message sent to foreman {foreman.first_name} {foreman.last_name}")
            except Exception as e:
                logger.error(f"Error sending message to foreman {foreman.first_name}: {e}")

            # Workers
            for worker in brigade.workers.all():
                try:
                    lang = BotUser.objects.get(telegram_id=worker.telegram_id).lang
                    text = build_task_message(
                        lang=lang,
                        title=instance.name,
                        description=(instance.description[:100] + "..." if len(instance.description) > 100 else instance.description),
                        deadline=instance.deadline.strftime("%d-%m-%Y")
                    )
                    send_message(chat_id=worker.telegram_id, text=text)
                    logger.info(f"Message sent to worker {worker.first_name} {worker.last_name}")
                except Exception as e:
                    logger.error(f"Error sending message to worker {worker.first_name}: {e}")


@receiver(pre_delete, sender=Task)
def save_task_details_on_finished_works(sender, instance, **kwargs):
    """
    Signal to save task details for it's finished works if the exist
    """

    instance.finished_works.update(task_name=instance.name)


@receiver(pre_delete, sender=Worker)
def save_worker_details_on_finished_works(sender, instance, **kwargs):
    """
    Signal to save worker details for it's finished works if the exist
    """

    instance.finished_works.update(worker_fullname=instance.full_name)


@receiver(pre_delete, sender=User)
def delete_bot_user_on_user_delete(sender, instance, **kwargs):
    bot_user = BotUser.objects.filter(telegram_id=instance.telegram_id)

    # Stop, if no BotUser found by telegram id
    if not bot_user.exists(): 
        return

    # Delete BotUser as well if user object from admin panel is deleted
    bot_user.first().delete()

