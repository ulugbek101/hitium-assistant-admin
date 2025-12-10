from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from .managers import UserManager


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

    DOCUMENT_TYPES = (
        ('passport', 'Passport'),
        ('id_card', 'ID Karta'),
    )

    ROLE_TYPES = (
        ('worker', 'Работник'),
        ('brigader', 'Бригадир'),
        ('admin', 'Админ'),
    )
    username = models.CharField(default="", null=True, blank=True, max_length=1)
    telegram_id = models.CharField(verbose_name="Телеграмм ID", max_length=255, unique=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=255, unique=True,
                                    help_text="Должен быть в формате 998996937308")

    first_name = models.CharField(verbose_name="Имя", max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    middle_name = models.CharField(verbose_name="Отчество", max_length=255)

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
    is_superuser = models.BooleanField(verbose_name="Статус муперпользователя", default=False)

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
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

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
