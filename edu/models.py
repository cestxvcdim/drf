from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='course_previews/', **NULLABLE, verbose_name='картинка')
    description = models.TextField(verbose_name='описание')

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='lesson_previews/', **NULLABLE, verbose_name='картинка')
    description = models.TextField(verbose_name='описание')
    video_link = models.URLField(verbose_name='ссылка на видео')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс')

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
