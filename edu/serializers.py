from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from edu.models import Course, Lesson
from edu.validators import LessonLinkValidator
from users.models import Subscription


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LessonLinkValidator(field='video_link')]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField(read_only=True)

    @staticmethod
    def get_is_subscribed(obj):
        return Subscription.objects.filter(course=obj).exists()

    @staticmethod
    def get_lessons_count(obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'author', 'lessons_count', 'is_subscribed', 'lessons')
