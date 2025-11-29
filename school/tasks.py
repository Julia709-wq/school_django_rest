from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Course, Subscription
from users.models import User


@shared_task
def send_course_update_notification(course_id):
    course_instance = Course.objects.get(id=course_id)
    subscription_instance = Subscription.objects.filter(course=course_instance)
    emails = [sub.user.email for sub in subscription_instance if sub.user.email]

    if not emails:
        return f"Нет оформленных подписок на курс {course_instance.name}"

    subject = f"Обновление материалов курса {course_instance.name}"
    message = (f"Здравствуйте! Уведомляем Вас о том, что в курс были добавлены новые материалы."
               f"Перейдите по ссылке для ознакомления: http://localhost:8000/school/{course_id}/")

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails
    )

    return "Пользователи успешно получили уведомление"


@shared_task
def deactivate_user():
    threshold_date = timezone.now() - timedelta(days=30)

    print(f"Текущее время: {timezone.now()}")
    print(f"Пороговая дата: {threshold_date}")

    inactive_users = User.objects.filter(
        last_login__lt=threshold_date,
        is_active=True
    )
    count_before = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Заблокировано {count_before} неактивных пользователей"

