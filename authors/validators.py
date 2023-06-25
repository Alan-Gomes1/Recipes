from collections import defaultdict

from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self):
        self.clean_preparation_time()
        self.clean_servings()
        data = self.data

        title = data.get('title')
        if len(title) < 5:
            self.errors['title'].append(
                'Title must be at least 5 characters long.'
            )

        description = data.get('description')
        if description is not None:
            if len(description) < 10:
                self.errors['description'].append(
                    'Description must be at least 10 characters long.'
                )

        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append(
                'Title and description must be different.'
            )

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors[field_name].append('Must be a positive number')

        return field_value
