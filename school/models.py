from django.db import models


class Lesson(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    video = models.CharField(verbose_name='ссылка')

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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


