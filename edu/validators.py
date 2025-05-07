from rest_framework.serializers import ValidationError

valid_prefix_links = ['https://youtube', 'https://youtu.be']


class LessonLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = dict(value).get(self.field)
        for prefix in valid_prefix_links:
            if link.startswith(prefix):
                return
        raise ValidationError('Ссылка ведет на непроверенный ресурс.')
