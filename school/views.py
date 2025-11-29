from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from school.models import Course, Lesson, Subscription, CoursePayment
from school.serializers import CourseSerializer, LessonSerializer, CoursePaymentSerializer
from school.services import create_course_payment
from users.permissions import IsModer, IsOwner, IsOwnerAndNotModer
from school.paginators import SchoolPaginator
from school.tasks import send_course_update_notification




class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = SchoolPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        if self.request.user.is_authenticated:
            course.owner = self.request.user
            course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner,]
        elif self.action == "destroy":
            self.permission_classes = [IsOwnerAndNotModer, ]
        return super().get_permissions()

    def perform_update(self, serializer):
        old_course = self.get_object()
        course = serializer.save()

        excluded_fields = ['updated_at', 'created_at', 'owner']
        changed_fields = []

        for field in course._meta.fields:
            if field.name not in excluded_fields:
                old_value = getattr(old_course, field.name)
                new_value = getattr(course, field.name)
                if old_value != new_value:
                    changed_fields.append(field.name)

        if changed_fields:
            send_course_update_notification.delay(course.id)

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        if self.request.user.is_authenticated:
            lesson.owner = self.request.user
            lesson.save()

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = SchoolPaginator

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionAPIView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(
                user=user,
                course=course_item
            )
            message = 'Подписка активирована'

        return Response({"message": message}, status=status.HTTP_200_OK)


class CoursePaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = CoursePaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            course_id = request.data.get('course_id')
            course = get_object_or_404(Course, id=course_id)

            existing_payment = CoursePayment.objects.filter(
                user=request.user,
                course=course,
                status='pending'
            ).first()

            if existing_payment:
                serializer = self.get_serializer(existing_payment)
                return Response(serializer.data, status=status.HTTP_200_OK)

            payment = create_course_payment(request.user, course)
            serializer = self.get_serializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

