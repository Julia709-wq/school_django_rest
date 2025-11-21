import stripe
from django.conf import settings
from school.models import CoursePayment


stripe.api_key = settings.STRIPE_API_KEY


def create_product(course_name, description=""):
    """Создание продукта для курса"""
    try:
        product = stripe.Product.create(
            name=course_name,
            description=description
        )
        return product
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании продукта: {str(e)}")


def create_price(amount, product_id):
    """Создание цены для курса"""
    try:
        converted_amount = int(amount * 100)
        price = stripe.Price.create(
            product=product_id,
            unit_amount=converted_amount,
            currency='rub'
        )
        return price
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании цены: {str(e)}")


def create_payment_session(price_id, success_url, cancel_url, metadata=None):
    """Создание сессии оплаты"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata or {}
        )
        return session
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании сессии: {str(e)}")


def create_course_payment(user, course):
    """Основная функция создания платежа"""
    try:
        product = create_product(
            course_name=course.name,
            description=course.description or ""
        )
        price = create_price(
            amount=course.price,
            product_id=product.id
        )

        success_url = f"{settings.FRONTEND_URL}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{settings.FRONTEND_URL}/payment/cancel/"

        session = create_payment_session(
            price_id=price.id,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'course_id': str(course.id),
                'user_id': str(user.id)
            }
        )

        payment = CoursePayment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            stripe_product_id=product.id,
            stripe_price_id=price.id,
            stripe_session_id=session.id,
            payment_url=session.url,
            status='pending'
        )

        return payment

    except Exception as e:
        raise Exception(f"Ошибка создания платежа: {str(e)}")

