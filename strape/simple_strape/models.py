from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Tax(models.Model):
    """ Модель налогов. """

    name = models.CharField(
        max_length=200,
        verbose_name='Название налога'
    )
    value = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, message='Налог не может быть меньше 1%'),
            MaxValueValidator(100, message='Налог не может быть больше 99%')
        ],
    )

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return f'{self.name}'


class Discount(models.Model):
    """ Модель скидок. """

    name = models.CharField(
        max_length=200,
        verbose_name='Название скидки'
    )
    value = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, message='Скидка не может быть меньше 1%'),
            MaxValueValidator(100, message='Скидка не может быть больше 100%')
        ],
    )

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    """ Модель товара. """
    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название товара'
    )
    description = models.TextField(
        verbose_name='Описание'
        )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES
        )
    price = models.IntegerField(
        verbose_name='Цена',
        validators=[
            MinValueValidator(50, message='Минимальное значение: 50'),
        ],
        )
    tax = models.ManyToManyField(
        Tax,
        verbose_name='Налоги',
    )
    discount = models.ManyToManyField(
        Discount,
        verbose_name='Скидки',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}'

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Order(models.Model):
    """Подборка товаров."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название подборки'
    )
    items = models.ManyToManyField(
        Item
    )

    class Meta:
        verbose_name = 'Подборка товаров'
        verbose_name_plural = 'Подборки товаров'

    def __str__(self):
        return f'{self.name}'
