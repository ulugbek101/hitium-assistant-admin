from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count

from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.filters.admin import RangeDateFilter

from .models import (
    Specialization, User, Brigade, Foreman, Worker, Day,
    Attendance, BotUser, Task, FinishedWork, FinishedWorkPhoto,
    ObjectPhoto, Object, Freshman
)

admin.site.unregister(Group)


class BaseUserAdmin(ModelAdmin):
    list_display = (
        "telegram_id", "first_name", "last_name",
        "middle_name", "phone_number", "role"
    )
    list_display_links = ("telegram_id",)
    search_fields = ("first_name", "last_name", "middle_name", "phone_number")
    search_help_text = "Telegram ID, Имя, Фамилия, Отчество ..."

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "telegram_id", "phone_number",
                "first_name", "last_name",
                "middle_name", "born_year",
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
    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]

    def has_add_permission(self, request):
        return False


@admin.register(Foreman)
class ForemanAdmin(BaseUserAdmin):
    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]


@admin.register(Worker)
class WorkerAdmin(BaseUserAdmin):
    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]

    def has_add_permission(self, request):
        return False


@admin.register(Specialization)
class SpecializationAdmin(ModelAdmin):
    list_display = ("name", "created", "updated")
    list_display_links = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию специализции (чувствительна к регистру)"

    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]

@admin.register(Brigade)
class BrigadeAdmin(ModelAdmin):
    list_display = ("name", "foreman", "workers_count")
    autocomplete_fields = ("foreman", "workers")
    search_fields = ("name", "foreman__first_name", "foreman__last_name", "foreman__middle_name")
    search_help_text = "Наименование бригад или ФИО бригадира"

    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            workers_count=Count("workers")
        )

    def workers_count(self, obj):
        return obj.workers_count

    workers_count.short_description = "Кол-во рабочих"

@admin.register(Day)
class DayAdmin(ModelAdmin):
    search_fields = ("date",)

    def has_add_permission(self, request):
        return False

@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    search_fields = [
        "worker__first_name",
        "worker__last_name",
        "worker__middle_name",
        "worker__phone_number",
    ]
    autocomplete_fields = ("day", "worker")
    search_help_text = "Имя сотрудника или номер телефона"

    list_display = ["worker", "get_is_absent", "start_time", "end_time", "day"]
    list_editable = ["start_time", "end_time"]
    list_filter_submit = True
    list_filter = ["day__date"]

    def has_add_permission(self, request):
        return False
    
    def get_is_absent(self, obj):
        return f"✅" if not obj.is_absent else "❌"

    get_is_absent.short_description = "Явился на работу"

@admin.register(BotUser)
class BotUserAdmin(ModelAdmin):
    search_fields = ["first_name", "last_name", "middle_name"]

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = ["pk", "name", "created", "deadline", "is_done"]
    list_display_links = ["pk", "name"]
    list_editable = ["is_done"]
    autocomplete_fields = ["brigades"]
    search_fields = ["name", "description", "deadline"]
    search_help_text = "Фрагмент из заголовка или описания задачи"

    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
        ["deadline", RangeDateFilter],
        "is_done",
    ]

    def pk(self, obj):
        return f"#{obj.pk}"

    pk.short_description = "ID"


class FinishedWorkPhotoInline(StackedInline):
    model = FinishedWorkPhoto
    extra = 0


@admin.register(FinishedWork)
class FinishedWorkAdmin(ModelAdmin):
    list_display = ["task", "task_deadline", "worker", "is_done"]
    list_display_links = ["task"]
    list_editable = ["is_done"]
    autocomplete_fields = ["task", "worker"]
    search_fields = ["task__name", "worker__full_name"]
    search_help_text = "Фрагмент из описания или ФИО сотрудника"
    inlines = [FinishedWorkPhotoInline]

    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
        "is_done",
    ]

    def task_deadline(self, obj):
        return obj.task.deadline

    task_deadline.short_description = "Дедлайн"


class ObjectPhotoInline(StackedInline):
    model = ObjectPhoto
    extra = 0


@admin.register(Object)
class ObjectAdmin(ModelAdmin):
    list_display = ["id", "name", "workers_count", "created", "updated"]
    list_display_links = ["id", "name"]
    autocomplete_fields = ["workers_involved"]
    search_fields = ["name"]
    search_help_text = "Наименование объекта"
    inlines = [ObjectPhotoInline]

    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]

    def workers_count(self, obj):
        return obj.workers_involved.count()

    workers_count.short_description = "Ко-во вовлеченных сотрудников"


@admin.register(Freshman)
class FreshmanAdmin(ModelAdmin):
    list_display = [
        "id", "fullname", "specialization",
        "phone_number", "created", "updated"
    ]
    list_display_links = ["id", "fullname"]
    autocomplete_fields = ["specialization"]
    search_fields = ["fullname", "specialization__name", "phone_number"]
    search_help_text = "Имя, специализация или номер телефона"

    list_filter_submit = True
    list_filter = [
        ["created", RangeDateFilter],
        ["updated", RangeDateFilter],
    ]
