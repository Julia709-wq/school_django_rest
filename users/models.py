from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from school.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    city = models.CharField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField(verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=200, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.amount}, {self.date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-date',)
