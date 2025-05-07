from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from edu.models import Course, Lesson
from users.models import Payment, User


class UsersTestCase(APITestCase):
    def setUp(self) -> None:
        """Setup"""

        """Users"""
        self.admin = User.objects.create(email='admin@org.com', password='332211', is_staff=True, is_superuser=True)
        self.user = User.objects.create(email='test@org.com', password='112233')

        self.client.force_authenticate(user=self.admin)
        self.client.force_authenticate(user=self.user)

        """Courses & Lessons"""
        self.course = Course.objects.create(
            title='test_course',
            description='test_course_description',
            author=self.admin
        )
        self.lesson = Lesson.objects.create(
            title='test_lesson',
            description='test_lesson_description',
            video_link='https://youtu.be/testvideolink',
            course=self.course,
            author=self.admin
        )

        """Payments"""
        self.payment1 = Payment.objects.create(
            user=self.user,
            paid_course=self.course,
            paid_lesson=None,
            payment_amount=8000,
            payment_method='card'
        )
        self.payment2 = Payment.objects.create(
            user=self.user,
            paid_course=None,
            paid_lesson=self.lesson,
            payment_amount=600,
            payment_method='cash'
        )

    def test_subscription_request(self):
        url = reverse('users:sub-courses', kwargs={'pk': self.course.id})
        post_data = {
            'course_id': self.course.id,
        }

        response1 = self.client.post(url, data=post_data)
        data1 = response1.json()

        response2 = self.client.post(url, data=post_data)
        data2 = response2.json()

        self.assertEqual(
            response1.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response2.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data1.get('message'), 'Подписка добавлена'
        )

        self.assertEqual(
            data2.get('message'), 'Подписка удалена'
        )
