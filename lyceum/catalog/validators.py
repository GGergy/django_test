import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.args = args

    def __call__(self, value):
        match = re.findall(r"\w+[А-я]+\w+", value.lower())
        for arg in self.args:
            if arg in match:
                return
        needs = "или".join([f"`{word}`" for word in self.args])
        raise ValidationError(f"В тексте должны быть слова {needs}")


class ValidateNormalizedNameByClass:
    patterns = {
        "A": "А",
        "E": "Е",
        "T": "Т",
        "O": "О",
        "P": "Р",
        "H": "Н",
        "K": "К",
        "X": "Х",
        "C": "С",
        "B": "В",
        "M": "М",
        "e": "е",
        "y": "у",
        "o": "о",
        "p": "р",
        "a": "а",
        "k": "к",
        "x": "х",
        "c": "с",
        "b": "ь",
        "m": "м",
    }

    def __init__(self, klass, item_id):
        self.item_type = klass
        self.item_id = item_id

    def __call__(self, value):
        normalized = self.normalize(value)
        names, normal_names = self.query()
        if normalized in normal_names:
            raise ValidationError(
                f"Элемент c похожим названием"
                f" ({names[normal_names.index(normalized)]})"
                f" уже существует. Рекомендуется использовать его",
            )
        return normalized

    def normalize(self, value: str):
        for letter in value:
            if letter in self.patterns:
                value = value.replace(letter, self.patterns[letter])
        value = "".join(re.findall(r"\w", value.lower()))
        if not value:
            raise ValidationError(
                "В теге должна присутствовать хотя бы одна буква или цифра",
            )
        normalized = value[0]
        for letter in value[1:]:
            if normalized[-1] != letter:
                normalized += letter
        return normalized

    def query(self):
        response = [
            (item.name, item.normalized_name)
            for item in self.item_type.objects.all()
            if item.id != self.item_id
        ]
        return [i[0] for i in response], [i[1] for i in response]


__all__ = []
