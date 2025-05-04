from django.db import models

# Константа для максимальной длины
MAX_LENGTH = 255

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'  # исправлено на правильное множественное число

class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование коллекции')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'  # исправлено на правильное множественное число

class Music(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование музыки')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    genre = models.CharField(max_length=MAX_LENGTH, verbose_name='Жанр')
    artist = models.CharField(max_length=MAX_LENGTH, verbose_name='Артист')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_exist = models.BooleanField(default=True, verbose_name='Доступность заказов')  # исправлено

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    collection = models.ManyToManyField(Collection, verbose_name='Коллекция')

    def __str__(self):
        return f"{self.name} - ({self.price} рублей)"

    class Meta:
        verbose_name = 'Музыка'
        verbose_name_plural = 'Музыки'  # исправлено на правильное множественное число
