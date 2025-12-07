from rest_framework import serializers

from school.models import Lesson, Course, Subscription, CoursePayment
from school.validators import LinkValidator


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'description', 'lessons_count', 'lessons', 'is_subscribed']
        read_only_field = ['owner', ]

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_field = ['owner',]
        validators = [LinkValidator(field="video")]


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'user', 'course', 'is_subscribed']


class CoursePaymentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = CoursePayment
        fields = [
            'id', 'course', 'course_name', 'amount', 'payment_url',
            'status', 'created_at', 'stripe_session_id'
        ]
        read_only_fields = [
            'id', 'course_name', 'amount', 'payment_url',
            'status', 'created_at', 'stripe_session_id'
        ]
