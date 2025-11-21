from django.conf import settings
from django.db import models


class Lesson(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    video = models.CharField(verbose_name='ссылка')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='владелец')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Course(models.Model):
    name = models.CharField(verbose_name='название')
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lessons = models.ManyToManyField(Lesson, verbose_name='уроки', blank=True, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100, verbose_name='цена')
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='владелец', related_name='курсы')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Subscription(models.Model):
    SUBSCRIPTION_OPTIONS = [
        ('basic', 'Базовая'),
        ('advanced', 'Расширенная'),
        ('family', 'Семейная')
    ]

    name = models.CharField(choices=SUBSCRIPTION_OPTIONS, default='basic')
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class CoursePayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('failed', 'Возникла ошибка при оплате')
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма')

    stripe_product_id = models.TextField(blank=True, null=True)
    stripe_price_id = models.TextField(blank=True, null=True)
    stripe_session_id = models.TextField(blank=True, null=True)

    payment_url = models.URLField(max_length=5000, blank=True, null=True, verbose_name='ссылка на оплату')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Платеж: {self.id} - {self.user} - {self.course}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
