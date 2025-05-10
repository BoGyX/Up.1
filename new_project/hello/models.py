from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

MAX_LENGTH = 255

class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser):
    login = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name="Логин")
    name = models.CharField(max_length=50, verbose_name="Имя")
    surname = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'surname', 'middle_name']

    def __str__(self):
        return f"{self.surname} {self.name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name="Категория")

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name="Производитель")

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name="Исполнитель")

    def __str__(self):
        return self.name

class VinylRecord(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, verbose_name="Название")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="Исполнитель")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на изображение")

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")

    def __str__(self):
        return f"Заказ #{self.id}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.login}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    vinyl = models.ForeignKey(VinylRecord, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.vinyl.title}"

    @property
    def subtotal(self):
        return self.vinyl.price * self.quantity

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    vinyl = models.ForeignKey(VinylRecord, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за штуку")

    def __str__(self):
        return f"{self.vinyl.title} ({self.quantity} шт.)"