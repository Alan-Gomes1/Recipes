from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Your username')
        add_attr(self.fields['email'], 'placeholder', 'Your e-mail')
        add_attr(self.fields['first_name'], 'placeholder', 'Ex.: John')
        add_attr(self.fields['last_name'], 'placeholder', 'Ex.: Doe')
        add_attr(self.fields['password'], 'placeholder',
                 'Type your password here')
        add_attr(self.fields['confirm_password'], 'placeholder',
                 'Repeat your password')

    username = forms.CharField(
        required=True,
        error_messages={
            'required': 'This field is required',
            'min_length': 'Make sure the value is at least 4 characters long.',
            'max_length': 'Username must have less than 150 characters.',
        },
        help_text=('Mandatory. Minimum 4 and maximum 150 characters.\
        Only letters, numbers and @/./+/-/_.'),
        label='Username',
        min_length=4, max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First name',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last name',
    )

    email = forms.EmailField(
        error_messages={'required': 'This field is required'},
        required=True,
        label='E-mail',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=("""
        Password must have at least one uppercase letter,
        one lowercase letter and one number. The length should be
        at last 8 characters.
        """),
        validators=[strong_password],
        label='Password',
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This field is required'
        },
        label='Confirm password',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError({
                'confirm_password': 'Password and confirm password must be equal'
            })
