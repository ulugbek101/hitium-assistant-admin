from django.utils.translation import override, gettext_lazy as _

from modeltranslation.translator import register, TranslationOptions
from api.models import Task

@register(Task)
class TaskTranslationOptions(TranslationOptions):
	fields = ('name', 'description')


def build_task_message(lang, title, description, deadline):
    """
    Function to manually build tranlsation to send message via Telegram API to user's telegram
    """

    with override(lang):
        text = f"<b><u>{_('Новая задача')}</u></b>\n\n"
        text += f"<b>{title}</b>\n"
        text += f"<i>{description}</i>\n\n"
        text += f"{_('Дата сдачи')}: <b>{deadline}</b>"

        if len(description) > 100:
                text += f"\n\n<i>{_('Что бы прочитать полностью, перейдите в раздел задач с командой /tasks')}</i>"

    return text
