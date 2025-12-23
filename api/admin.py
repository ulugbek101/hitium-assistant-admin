from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from django.db.models import Count

from .models import Specialization, User, Brigade, Foreman, Worker


admin.site.unregister(Group)


class BaseUserAdmin(ModelAdmin):
    list_display = ("telegram_id", "first_name", "last_name", "middle_name", "phone_number", "role")
    list_display_links = ("telegram_id",)
    search_fields = ("first_name", "last_name", "middle_name", "phone_number")
    list_filter = ("created", "updated")
    search_help_text = "Telegram ID, Имя, Фамилия, Отчество ..."

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "telegram_id",
                "phone_number",
                "first_name",
                "last_name",
                "middle_name",
                "born_year",
            )
        }),
        ("Документы", {
            "fields": (
                "passport_photo",
                "id_card_photo1",
                "id_card_photo2",
            )
        }),
        ("Финансы", {
            "fields": (
                "card_number",
                "card_holder_name",
                "tranzit_number",
                "bank_name",
            )
        }),
        ("Работа", {
            "fields": ("role", "specialization")
        }),
        ("Статус", {
            "fields": ("is_active", "is_staff")
        }),
    )

    def role(self, obj):
        return obj.get_role_display()
    role.short_description = "Роль"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Foreman)
class ForemanAdmin(BaseUserAdmin):
    pass


@admin.register(Worker)
class ForemanAdmin(BaseUserAdmin):
    pass



@admin.register(Specialization)
class SpecializationAdmin(ModelAdmin):
    list_display = ("name", "created", "updated")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("created", "updated")
    search_help_text = "Поиск по названию специализции (чувствительна к регистру)"


@admin.register(Brigade)
class BrigadeAdmin(ModelAdmin):
    list_display = ("name", "foreman", "workers_count")
    autocomplete_fields = ("foreman", "workers")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(workers_count=Count("workers"))

    def workers_count(self, obj):
        return obj.workers_count

    workers_count.short_description = "Кол-во рабочих"
