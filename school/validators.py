import re
from rest_framework.validators import ValidationError


class LinkValidator():
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
        # https://youtu.be/bt4RA3z8cU8?si=hnV-bnqjVLdPNOEM такая ссылка пройдет валидацию
        tmp_val = dict(value).get(self.field)
        if not bool(re.match(pattern, tmp_val)):
            raise ValidationError("Ссылка не прошла валидацию")
