from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):  # normal user
    def create_user(self, email, name, password=None):  # constructor

        if not email:
            raise ValueError('No email address found')

        if not name:
            raise ValueError('No name found')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)  # set password
        user.save(using=self._db)  # save user in database
        return user

    def create_superuser(self, email, name, password):  # admin user
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_student = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()

    def __str__(self):  # when i create a user object, and call it, what will show
        return self.email

    def has_perm(self, perm, obj=None):  # for permission
        return True

    def has_module_perms(self, app_label):
        return True


class StudentProfileModel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)  # 1 user have only 1 profile model
    image = models.ImageField(null=True, blank=True)
    varsity_name = models.CharField(max_length=255, null=True, blank=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)


class PublisherProfileModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    book_count = models.IntegerField(default=0)

    def __str__(self):  # when i create a user object, and call it, what will show
        return self.user.name
