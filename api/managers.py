from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number, **extra_fields)

        if password:
            user.password = make_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, password, **extra_fields)


class ForemanManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="foreman")


class WorkerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="worker")

