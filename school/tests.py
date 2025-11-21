from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.com',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            "name": "Test Lesson",
            "description": "Test",
            "video": "Test link"
        }

        response = self.client.post('/lesson/create/', data=data)


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {'id': 1, 'name': 'Test Lesson', 'description': 'Test', 'image': None, 'video': 'Test link', 'owner': self.user.id}
        )

        self.assertTrue(Lesson.objects.all().exists())


    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""

        lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test",
            video="Test link",
            owner=self.user
        )

        response = self.client.get("/lesson/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            [{'id': lesson.id, 'name': 'Test Lesson', 'description': 'Test', 'image': None, 'video': 'Test link', 'owner': self.user.id}]
        )


    def test_update_lesson(self):
        """Тестирование обновления данных об уроке"""
        lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test",
            video="Test link",
            owner=self.user
        )

        data = {
            "name": "Test2"
        }

        response = self.client.patch(f"/lesson/update/{lesson.id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'id': lesson.id, 'name': 'Test2', 'description': 'Test', 'image': None, 'video': 'Test link', 'owner': self.user.id}
        )


    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test",
            video="Test link",
            owner=self.user
        )

        response = self.client.delete(f"/lesson/delete/{lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Lesson.objects.all().exists())


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.com',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тестирование создания курса"""
        data = {
            "name": "Test Course",
            "description": "Test"
        }

        response = self.client.post('/school/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {'id': 1, 'name': 'Test Course', 'image': None, 'description': 'Test', 'lessons_count': 0, 'lessons': []}
        )

        self.assertTrue(Course.objects.all().exists())


    def test_list_course(self):
        """Тестирование вывода списка курсов"""
        course = Course.objects.create(
            name="Test course",
            description="Test"
        )

        response = self.client.get("/school/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            [{'id': course.id, 'name': 'Test course', 'image': None, 'description': 'Test', 'lessons_count': 0, 'lessons': []}]
        )

    def test_update_course(self):
        """Тестирование обновления данных о курсе"""
        course = Course.objects.create(
            name="Test course",
            description="Test",
            owner=self.user
        )

        data = {
            "name": "Test2"
        }

        response = self.client.patch(f"/school/{course.id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'id': course.id, 'name': 'Test2', 'image': None, 'description': 'Test', 'lessons_count': 0, 'lessons': []}
        )


    def test_delete_course(self):
        """Тестирование удаления курса"""

        course = Course.objects.create(
            name="Test course",
            description="Test",
            owner=self.user
        )

        print(f"User groups: {list(self.user.groups.all())}")
        print(f"Is moder: {self.user.groups.filter(name='moders').exists()}")
        print(f"Is owner: {course.owner == self.user}")

        response = self.client.delete(f"/school/{course.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Course.objects.all().exists())
