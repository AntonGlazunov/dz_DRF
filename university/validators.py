import re
from rest_framework.serializers import ValidationError


class VideoURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'https://www.youtube.com/\S')
        url_str = str(dict(value).get(self.field))
        if not bool(reg.match(url_str)):
            raise ValidationError("Не верно указана ссылка")

