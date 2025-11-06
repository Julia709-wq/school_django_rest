from django.core.management.base import BaseCommand
from users.models import Payment, Course, Lesson, User


class Command(BaseCommand):
    help = 'Add payments to DB'

    def handle(self, *args, **kwargs):
        user1, _ = User.objects.get_or_create(
            email='user1@mail.com',
            phone_number='+79998999915',
            city='Moscow'
        )

        user2, _ = User.objects.get_or_create(
            email='user2@mail.com',
            phone_number='+79997999914',
            city='Rostov'
        )

        course, _ = Course.objects.get_or_create(name='Графический дизайнер', description='...')
        lesson, _ = Lesson.objects.get_or_create(name='Урок 1. Введение', description=',,,')

        payments = [
            {'user': user1, 'date': '2024-09-09', 'course': course, 'amount': 80000, 'payment_method': 'Материнский капитал'},
            {'user': user2, 'date': '2024-09-09', 'lesson': lesson, 'amount': 1500, 'payment_method': 'Перевод'},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Payment {payment.amount} was created'))
            else:
                self.stdout.write(self.style.WARNING(f'Payment {payment.amount} already exists'))

