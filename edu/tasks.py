from celery import shared_task
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from config.settings import EMAIL_HOST_USER
from edu.models import Course
from users.models import Subscription


@shared_task
def send_course_update_notification(course_id):
    course_item = get_object_or_404(Course, pk=course_id)
    subscribed_users = Subscription.objects.filter(course=course_item)

    for subscription in subscribed_users:
        subject = 'Обновление материалов курса'
        message = f'Материалы курса {subscription.course.title} были обновлены. Проверьте новые материалы!'
        send_mail(subject, message, EMAIL_HOST_USER, [subscription.user.email])
