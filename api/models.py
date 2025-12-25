from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .managers import UserManager, ForemanManager, WorkerManager


ROLE_TYPES = (
    ('worker', 'Работник'),
    ('foreman', 'Бригадир'),
    ('admin', 'Админ'),
)

DOCUMENT_TYPES = (
    ('passport', 'Passport'),
    ('id_card', 'ID Karta'),
)


class BotUser(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.CharField(max_length=255, unique=True)
    lang = models.CharField(max_length=2, default='uz')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    born_year = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    type_of_document = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    card_holder_name = models.CharField(max_length=100, null=True, blank=True)
    tranzit_number = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=20, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    id_card_photo1 = models.CharField(max_length=255, null=True, blank=True)
    id_card_photo2 = models.CharField(max_length=255, null=True, blank=True)
    passport_photo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "users"
        verbose_name = "Рабочий"
        verbose_name_plural = "Рабочие"
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"


class Specialization(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
        ordering = ("-created",)


class User(AbstractBaseUser, PermissionsMixin):

    DOCUMENT_TYPES = DOCUMENT_TYPES
    ROLE_TYPES = ROLE_TYPES

    username = models.CharField(default="", null=True, blank=True, max_length=1)
    telegram_id = models.CharField(verbose_name="Телеграмм ID", max_length=255, unique=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=255, unique=True,
                                    help_text="Должен быть в формате 998996937308")

    first_name = models.CharField(verbose_name="Имя", max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    middle_name = models.CharField(verbose_name="Отчество", max_length=255)

    born_year = models.DateField(verbose_name="Дата рождения")

    type_of_document = models.CharField(verbose_name="Тип документа",
                                        max_length=50, choices=DOCUMENT_TYPES)

    card_number = models.CharField(verbose_name="Номер карты", max_length=16)
    card_holder_name = models.CharField(verbose_name="Носитель карты", max_length=255)
    tranzit_number = models.CharField(verbose_name="Транзитный номер", max_length=255)
    bank_name = models.CharField(verbose_name="Наименование банка", max_length=255)

    specialization = models.ForeignKey(
        Specialization, verbose_name="Специализация",
        on_delete=models.PROTECT, null=True,
    )

    role = models.CharField(verbose_name="Роль", max_length=50, choices=ROLE_TYPES, default='worker')

    passport_photo = models.ImageField(verbose_name="Фото пасспорта", upload_to='photos/', null=True, blank=True)
    id_card_photo1 = models.ImageField(verbose_name="Фото ID карты (лицевая часть)", upload_to='photos/', null=True, blank=True)
    id_card_photo2 = models.ImageField(verbose_name="Фото ID карты (задняя часть)", upload_to='photos/', null=True, blank=True)

    is_staff = models.BooleanField(verbose_name="Статус сотрудника", default=False,
                                   help_text="Может ли сотрудник заходить в админ панель")
    is_active = models.BooleanField(verbose_name="Статус активности пользователя", default=True)
    is_superuser = models.BooleanField(verbose_name="Статус cуперпользователя", default=False)

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата обновления", auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['telegram_id', 'first_name', 'last_name', 'middle_name', 'type_of_document',
                       'card_number', 'card_holder_name', 'tranzit_number', 'bank_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @property
    def username(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["telegram_id"]),
        ]
        ordering = ("-created",)


class Foreman(User):
    objects = ForemanManager()

    class Meta:
        proxy = True
        verbose_name = _("Бригадир")
        verbose_name_plural = _("Бригадиры")


    def save(self, *args, **kwargs):
        self.role = "foreman"
        super().save(*args, **kwargs)


class Worker(User):
    objects = WorkerManager()

    class Meta:
        proxy = True
        verbose_name = _("Работник")
        verbose_name_plural = _("Работники")


    def save(self, *args, **kwargs):
        self.role = "worker"
        super().save(*args, **kwargs)


class Brigade(models.Model):
    name = models.CharField(verbose_name=_("Назвние"), help_text=_("Дайте название бригаде"), unique=True)
    foreman = models.OneToOneField(verbose_name=_("Бригадир"), to=Foreman, related_name="brigade", on_delete=models.PROTECT, help_text=_("Выберите бригадира"))
    workers = models.ManyToManyField(verbose_name=_("Рабочие"), to=Worker, related_name="worker_brigade", help_text=_("Выберите рабочих"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Бригада")
        verbose_name_plural = _("Бригады")
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Day(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Дата рабочего дня")

    class Meta:
        db_table = "days"
        verbose_name = "Рабочий день"
        verbose_name_plural = "Рабочие дни"
        managed = False

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(BotUser, on_delete=models.CASCADE, db_column="worker", verbose_name="Рабочий")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, db_column="day", verbose_name="Рабочий день")
    is_absent = models.BooleanField(default=True, verbose_name="Отсутсвует", help_text="Если работник ЯВИЛСЯ на работу, то надо ОТКЛЮЧТЬ")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Время начала работы", help_text="Когда работник начал рабочий день")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Время завершения работы", help_text="Когда работник завершил рабочий день")

    class Meta:
        db_table = "attendance"
        verbose_name = "Отметка"
        verbose_name_plural = "Отметки"
        managed = False

    def __str__(self):
        return f"{self.worker.first_name} - {self.day.date.strftime("%Y-%m-%d")} - {'✅' if self.is_absent else '❌'}"


class Task(models.Model):
    name = models.CharField(verbose_name="Название задачи", help_text="Краткое описание задачи")
    description = models.TextField(verbose_name="Описание", help_text="Подробное описание задачи")
    brigades = models.ManyToManyField(verbose_name="Бригады", to=Brigade, help_text="Бригады, которые) будут заниматься задачей")
    is_done = models.BooleanField(verbose_name="Завершено")
    deadline = models.DateField(verbose_name="Дедлайн", help_text="Дата завершения работы")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return f"{self.name[:50]} - {self.brigade.name}"
