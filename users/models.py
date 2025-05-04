from django.contrib.auth.models import AbstractUser
from django.db import models

from edu.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}
PAYMENT_CHOICES = (
    ('cash', 'Наличные'),
    ('card', 'Перевод'),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone_number = models.CharField(max_length=12, **NULLABLE, verbose_name='номер телефона')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='фото профиля')

    token = models.CharField(max_length=100, **NULLABLE, verbose_name='токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='пользователь')

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')

    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный урок')

    payment_amount = models.FloatField(verbose_name='сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_CHOICES, verbose_name='способ оплаты')
