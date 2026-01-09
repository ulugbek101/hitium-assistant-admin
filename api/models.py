from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .managers import UserManager, ForemanManager, WorkerManager


ROLE_TYPES = (
    ('worker', _("Работник")),
    ('foreman', _("Бригадир")),
    ('admin', _("Админ")),
)

DOCUMENT_TYPES = (
    ('passport', _("Passport")),
    ('id_card', _("ID Karta")),
)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .managers import UserManager, ForemanManager, WorkerManager


ROLE_TYPES = (
    ('worker', _("Работник")),
    ('foreman', _("Бригадир")),
    ('admin', _("Администратор")),
)

DOCUMENT_TYPES = (
    ('passport', _("Паспорт")),
    ('id_card', _("ID карта")),
)


class BotUser(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.CharField(_("Telegram ID"), max_length=255, unique=True)
    lang = models.CharField(_("Язык"), max_length=2, default='uz')
    first_name = models.CharField(_("Имя"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Фамилия"), max_length=50, null=True, blank=True)
    middle_name = models.CharField(_("Отчество"), max_length=50, null=True, blank=True)
    born_year = models.DateField(_("Дата рождения"), null=True, blank=True)
    phone_number = models.CharField(_("Номер телефона"), max_length=12, null=True, blank=True)
    type_of_document = models.CharField(_("Тип документа"), max_length=20, null=True, blank=True)
    card_number = models.CharField(_("Номер карты"), max_length=16, null=True, blank=True)
    card_holder_name = models.CharField(_("Владелец карты"), max_length=100, null=True, blank=True)
    tranzit_number = models.CharField(_("Транзитный номер"), max_length=50, null=True, blank=True)
    bank_name = models.CharField(_("Название банка"), max_length=50, null=True, blank=True)
    specialization = models.CharField(_("Специализация"), max_length=255, null=True, blank=True)
    id_card_photo1 = models.CharField(_("Фото ID карты (лицевая сторона)"), max_length=255, null=True, blank=True)
    id_card_photo2 = models.CharField(_("Фото ID карты (обратная сторона)"), max_length=255, null=True, blank=True)
    passport_photo = models.CharField(_("Фото паспорта"), max_length=255, null=True, blank=True)

    class Meta:
        db_table = "users"
        verbose_name = _("Работник (Telegram)")
        verbose_name_plural = _("Работники (Telegram)")
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"


class Specialization(models.Model):
    name = models.CharField(verbose_name=_("Название специализации"), max_length=255)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания"))
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Дата обновления"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Специализация")
        verbose_name_plural = _("Специализации")
        ordering = ("-created",)


class User(AbstractBaseUser, PermissionsMixin):

    DOCUMENT_TYPES = DOCUMENT_TYPES
    ROLE_TYPES = ROLE_TYPES

    username = models.CharField(
        default="", null=True, blank=True, max_length=1)
    telegram_id = models.CharField(verbose_name=_(
        "Телеграмм ID"), max_length=255, unique=True)
    phone_number = models.CharField(
        verbose_name=_("Номер телефона"),
        max_length=255,
        unique=True,
        help_text=_("Должен быть в формате 998996937308"),
    )

    first_name = models.CharField(verbose_name=_("Имя"), max_length=255)
    last_name = models.CharField(verbose_name=_("Фамилия"), max_length=255)
    middle_name = models.CharField(verbose_name=_("Отчество"), max_length=255)

    born_year = models.DateField(verbose_name=_("Дата рождения"))

    type_of_document = models.CharField(
        verbose_name=_("Тип документа"),
        max_length=50,
        choices=DOCUMENT_TYPES,
    )

    card_number = models.CharField(
        verbose_name=_("Номер карты"), max_length=16)
    card_holder_name = models.CharField(
        verbose_name=_("Носитель карты"), max_length=255)
    tranzit_number = models.CharField(
        verbose_name=_("Транзитный номер"), max_length=255)
    bank_name = models.CharField(verbose_name=_(
        "Наименование банка"), max_length=255)

    specialization = models.ForeignKey(
        Specialization,
        verbose_name=_("Специализация"),
        on_delete=models.PROTECT,
        null=True,
    )

    role = models.CharField(
        verbose_name=_("Роль"),
        max_length=50,
        choices=ROLE_TYPES,
        default='worker',
    )

    passport_photo = models.ImageField(
        verbose_name=_("Фото пасспорта"),
        upload_to='photos/',
        null=True,
        blank=True,
    )
    id_card_photo1 = models.ImageField(
        verbose_name=_("Фото ID карты (лицевая часть)"),
        upload_to='photos/',
        null=True,
        blank=True,
    )
    id_card_photo2 = models.ImageField(
        verbose_name=_("Фото ID карты (задняя часть)"),
        upload_to='photos/',
        null=True,
        blank=True,
    )

    is_staff = models.BooleanField(
        verbose_name=_("Статус сотрудника"),
        default=False,
        help_text=_("Может ли сотрудник заходить в админ панель"),
    )
    is_active = models.BooleanField(verbose_name=_(
        "Статус активности пользователя"), default=True)
    is_superuser = models.BooleanField(verbose_name=_(
        "Статус cуперпользователя"), default=False)

    created = models.DateTimeField(
        verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_(
        "Дата обновления"), auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [
        'telegram_id',
        'first_name',
        'last_name',
        'middle_name',
        'type_of_document',
        'card_number',
        'card_holder_name',
        'tranzit_number',
        'bank_name',
    ]

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
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
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
    name = models.CharField(
        verbose_name=_("Назвние"),
        help_text=_("Дайте название бригаде"),
        unique=True,
    )
    foreman = models.OneToOneField(
        verbose_name=_("Бригадир"),
        to=Foreman,
        related_name="brigade",
        on_delete=models.PROTECT,
        help_text=_("Выберите бригадира"),
    )
    workers = models.ManyToManyField(
        verbose_name=_("Рабочие"),
        to=Worker,
        related_name="worker_brigade",
        help_text=_("Выберите рабочих"),
    )
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now_add=True)

    class Meta:
        verbose_name = _("Бригада")
        verbose_name_plural = _("Бригады")
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Day(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name=_("Дата рабочего дня"))

    class Meta:
        db_table = "days"
        verbose_name = _("Рабочий день")
        verbose_name_plural = _("Рабочие дни")
        managed = False

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        db_column="worker",
        verbose_name=_("Рабочий"),
    )
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        db_column="day",
        verbose_name=_("Рабочий день"),
    )
    is_absent = models.BooleanField(
        default=True,
        verbose_name=_("Отсутсвует"),
        help_text=_("Если работник ЯВИЛСЯ на работу, то надо ОТКЛЮЧТЬ"),
    )
    start_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_("Время начала работы"),
        help_text=_("Когда работник начал рабочий день"),
    )
    end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_("Время завершения работы"),
        help_text=_("Когда работник завершил рабочий день"),
    )

    class Meta:
        db_table = "attendance"
        verbose_name = _("Отметка")
        verbose_name_plural = _("Отметки")
        managed = False

    def __str__(self):
        return f"{self.worker.first_name} - {self.day.date.strftime('%Y-%m-%d')} - {'✅' if self.is_absent else '❌'}"


class Task(models.Model):
    name = models.CharField(
        verbose_name=_("Название задачи"),
        help_text=_("Краткое описание задачи"),
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Подробное описание задачи"),
    )
    brigades = models.ManyToManyField(
        verbose_name=_("Бригады"),
        to=Brigade,
        help_text=_("Бригады, которые будут заниматься задачей"),
    )
    is_done = models.BooleanField(verbose_name=_("Завершено"))
    deadline = models.DateField(
        verbose_name=_("Дедлайн"),
        help_text=_("Дата завершения работы"),
    )
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)

    class Meta:
        ordering = ["is_done", "-created"]
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")

    def __str__(self):
        return f"{self.name[:50]}"


class FinishedWork(models.Model):
    task = models.ForeignKey(verbose_name=_("Задача"), to=Task, on_delete=models.SET_NULL, null=True, related_name="finished_works")
    task_name = models.CharField(verbose_name=_("Название задачи"), max_length=255, null=True, blank=True, help_text=_("Пожалуйста, не заполняйте это поле, оно заполниться автоматически"))
    worker = models.ForeignKey(verbose_name=_("Работник, который сделал работу"), to=Worker, on_delete=models.SET_NULL, null=True, related_name="finished_works")
    worker_fullname = models.CharField(verbose_name=_("Работник, который сделал работу"), max_length=255, null=True, blank=True, help_text=_("Пожалуйста, не заполняйте это поле, оно заполниться автоматически"))
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True, help_text=_("Необязательное поле"))
    is_done = models.BooleanField(verbose_name=_("Принято"), default=False)
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)


    def __str__(self):
        return f"{_('Завершенная задача')} #{self.pk}"

    class Meta:
        ordering = ["-is_done", "-created"]
        verbose_name = _("Завершенная задача")
        verbose_name_plural = _("Завершенные задачи")


class FinishedWorkPhoto(models.Model):
    finished_work = models.ForeignKey(verbose_name=_("Завершенная работа"), to=FinishedWork, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Фото"), upload_to="media/", null=True, blank=True)
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)

    def __str__(self):
        return f"Фото #{self.pk} проделанной работы #{self.finished_work.pk}"

    class Meta:
        verbose_name = _("Фото проделанной работы")
        verbose_name_plural = _("Фото проделанных работ")


class Object(models.Model):
    name = models.CharField(verbose_name=_("Наименование объекта"), max_length=255)
    service_type = models.CharField(verbose_name=_("Тип оказываемой услуги"), max_length=255)
    responsible_person_details = models.CharField(verbose_name=_("Данные ответсвенной персоны"), max_length=255)
    workers_involved = models.ManyToManyField(verbose_name=_("Вовлеченные сотруники"), to=Worker)
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.created.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Объект")
        verbose_name_plural = _("Объекты")


class ObjectPhoto(models.Model):
    object = models.ForeignKey(verbose_name=_("Завершенная работа"), to=Object, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Фото"), upload_to="media/", null=True, blank=True)
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)

    def __str__(self):
        return f"Фото #{self.pk} объекта {self.object.name} созданный в {self.created.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Фото объекта")
        verbose_name_plural = _("Фото объекта")



class Freshman(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(verbose_name=_("Полное имя"), max_length=255)
    phone_number = models.CharField(verbose_name=_("Номер телефона"), max_length=13, help_text=_("Не принимает больше чем 13 символов, например: +998996937308"))
    specialization = models.ForeignKey(verbose_name=_("Специализация"), to=Specialization, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Дата обновления"), auto_now=True)

    def __str__(self):
        return f"Кандидат #{self.id} - {self.fullname} - {self.phone_number}"

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Кандидат")
        verbose_name_plural = _("Кандидаты")
