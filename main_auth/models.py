from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# Create your models here.


class Role(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'admin'),

        ('AGENCY', 'agency'),
        ('REALTOR', 'realtor'),

        ('BUILDER', 'builder'),
        ('MANAGER', 'manager'),
        ('SALE_MANGER', 'sale manager'),

        ('BANK', 'bank'),
        ('MODERATOR', 'moderator')
    )
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'roles'


class UserStatus(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_status'

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('The phone number field must be set'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # phone = models.CharField(max_length=14, unique=True, validators=[validate_phone,])
    phone = models.CharField(max_length=14, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    sure_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=240)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, default=2)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'sure_name', 'email', 'role_id']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # def clean(self):
    #     print(self, 'clean method')
    #     return self

    def save(self, *args, **kwargs):
        # my_function(self.my_field)
        # self.full_clean()
        # if CustomUser.objects.filter(phone=self.phone).exists():
        #     raise ValidationError('This value already exists in the database.')
        super().save(*args, **kwargs)
    # name = models.CharField(max_length=15)
    # email = models.EmailField(_("email address"), unique=True)
    # phone = models.CharField(max_length=14, unique=True)
    # status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, default=2)
    # role = models.ForeignKey(Role, on_delete=models.PROTECT)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username", "phone", "first_name", "role_id"]
    # USERNAME_FIELD = "phone"
    # REQUIRED_FIELDS = ["phone", "role_id"]

# class UserStatus(models.Model):
#     id = models.SmallAutoField(primary_key=True)
#     name = models.CharField(max_length='15', blank=True)



