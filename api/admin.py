from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from .models import Specialization, User


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("telegram_id", "first_name", "last_name", "middle_name", "phone_number", "role")
    list_display_links = ("telegram_id",)
    search_fields = ("first_name", "last_name", "middle_name", "phone_number")
    list_filter = ("created", "updated")
    search_help_text = "Telegram ID, Имя, Фамилия, Отчество ..."

    def role(self):
        UserAdmin.role.short_description = "Роль"
        return self.get_role_display()


@admin.register(Specialization)
class SpecializationAdmin(ModelAdmin):
    list_display = ("name", "created", "updated")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("created", "updated")
    search_help_text = "Поиск по названию специализции (чувствительна к регистру)"
