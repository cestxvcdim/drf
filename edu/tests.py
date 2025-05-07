from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from edu.models import Course, Lesson
from users.models import User


class EduTestCase(APITestCase):
    def setUp(self) -> None:
        """Setup"""

        """Users"""
        self.admin = User.objects.create(email='admin@org.com', password='332211', is_staff=True, is_superuser=True)
        self.user = User.objects.create(email='test@org.com', password='112233')
        self.author = User.objects.create(email='author@org.com', password='998877')

        self.client.force_authenticate(user=self.admin)
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.author)

        """Courses"""
        self.course1 = Course.objects.create(
            title='t1_course',
            description='t1_course_description',
            author=self.author
        )
        self.course2 = Course.objects.create(
            title='t2_course',
            description='t2_course_description',
            author=self.author
        )

        """Lessons"""
        self.lesson1_c1 = Lesson.objects.create(
            title='t1c1_lesson',
            description='t1c1_lesson_description',
            video_link='https://youtu.be/t1c1videolink',
            course=self.course1,
            author=self.author
        )
        self.lesson2_c1 = Lesson.objects.create(
            title='t2c1_lesson',
            description='t2c1_lesson_description',
            video_link='https://youtu.be/t2c1videolink',
            course=self.course1,
            author=self.author
        )

        self.lesson1_c2 = Lesson.objects.create(
            title='t1c2_lesson',
            description='t1c2_lesson_description',
            video_link='https://youtu.be/t1c2videolink',
            course=self.course2,
            author=self.author
        )
        self.lesson2_c2 = Lesson.objects.create(
            title='t2c2_lesson',
            description='t2c2_lesson_description',
            video_link='https://youtu.be/t2c2videolink',
            course=self.course2,
            author=self.author
        )

    def test_course_list(self):
        url = reverse('edu:course-list')
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course1.id,
                    "title": self.course1.title,
                    "preview": self.course1.preview,
                    "description": self.course1.description,
                    "author": self.author.id,
                },
                {
                    "id": self.course2.id,
                    "title": self.course2.title,
                    "preview": self.course2.preview,
                    "description": self.course2.description,
                    "author": self.author.id,
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            result, data
        )

    def test_course_retrieve(self):
        url = reverse('edu:course-detail', kwargs={'pk': self.course1.pk})
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), self.course1.title
        )

        self.assertEqual(
            data.get('author'), self.course1.author.id
        )

        self.assertEqual(
            data.get('lessons_count'), 2
        )

    def test_course_create(self):
        url = reverse('edu:course-list')
        create_data = {
            'title': 'new_course',
            'description': 'new_course_description',
            'author': self.author.id,
        }
        response = self.client.post(url, data=create_data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            Course.objects.all().count(), 3
        )

    def test_course_update(self):
        url = reverse('edu:course-detail', kwargs={'pk': self.course2.pk})
        update_data = {
            'title': 'updated_course',
            'description': 'updated_course_description',
        }
        response = self.client.patch(url, data=update_data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), 'updated_course'
        )

    def test_course_delete(self):
        url = reverse('edu:course-detail', kwargs={'pk': self.course2.pk})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Course.objects.all().count(), 1
        )

    def test_lesson_list(self):
        url = reverse('edu:lesson-list')
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 4,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson1_c1.id,
                    "title": self.lesson1_c1.title,
                    "preview": self.lesson1_c1.preview,
                    "description": self.lesson1_c1.description,
                    "video_link": self.lesson1_c1.video_link,
                    "course": self.course1.id,
                    "author": self.author.id
                },
                {
                    "id": self.lesson2_c1.id,
                    "title": self.lesson2_c1.title,
                    "preview": self.lesson2_c1.preview,
                    "description": self.lesson2_c1.description,
                    "video_link": self.lesson2_c1.video_link,
                    "course": self.course1.id,
                    "author": self.author.id
                },
                {
                    "id": self.lesson1_c2.id,
                    "title": self.lesson1_c2.title,
                    "preview": self.lesson1_c2.preview,
                    "description": self.lesson1_c2.description,
                    "video_link": self.lesson1_c2.video_link,
                    "course": self.course2.id,
                    "author": self.author.id
                },
                {
                    "id": self.lesson2_c2.id,
                    "title": self.lesson2_c2.title,
                    "preview": self.lesson2_c2.preview,
                    "description": self.lesson2_c2.description,
                    "video_link": self.lesson2_c2.video_link,
                    "course": self.course2.id,
                    "author": self.author.id
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            result, data
        )

    def test_lesson_retrieve(self):
        url = reverse('edu:lesson-retrieve', kwargs={'pk': self.lesson2_c1.pk})
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), self.lesson2_c1.title
        )

        self.assertEqual(
            data.get('author'), self.lesson2_c1.author.id
        )

        self.assertEqual(
            data.get('course'), self.lesson2_c1.course.id
        )

    def test_lesson_create(self):
        url = reverse('edu:lesson-create')
        create_data = {
            'title': 'new_lesson',
            'description': 'new_lesson_description',
            'video_link': 'https://youtu.be/newvideolink',
            'course': self.course2.id,
        }
        response = self.client.post(url, data=create_data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(), 5
        )

    def test_lesson_update(self):
        url = reverse('edu:lesson-update', kwargs={'pk': self.lesson1_c2.pk})
        update_data = {
            'title': 'updated_lesson',
            'description': 'updated_lesson_description',
            'video_link': 'https://youtu.be/updatedvideolink',
        }
        response = self.client.patch(url, data=update_data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'), 'updated_lesson'
        )

    def test_lesson_delete(self):
        url = reverse('edu:lesson-delete', kwargs={'pk': self.lesson2_c2.pk})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(), 3
        )
