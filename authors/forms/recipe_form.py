from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Units', 'Units'),
                    ('People', 'People'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                ),
            ),
        }

    def clean(self):
        super_clean = super().clean()
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must be at least 5 characters long.'
            )

        description = cleaned_data.get('description')
        if len(description) < 10:
            self._my_errors['description'].append(
                'Description must be at least 10 characters long.'
            )

        preparation_time = cleaned_data.get('preparation_time')
        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Preparation time must be a positive number.'
            )

        servings = cleaned_data.get('servings')
        if not is_positive_number(servings):
            self._my_errors['servings'].append(
                'Servings must be a positive number.'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
