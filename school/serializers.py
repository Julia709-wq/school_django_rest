from rest_framework import serializers

from school.models import Lesson, Course
from users.models import Payment


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, instance):
        return instance.lessons.count()


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

