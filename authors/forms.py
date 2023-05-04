from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    field.widget.attrs[attr_name] = attr_new_val.strip()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Your username')
        add_attr(self.fields['email'], 'placeholder', 'Your e-mail')
        add_attr(self.fields['first_name'], 'placeholder', 'Ex.: John')
        add_attr(self.fields['last_name'], 'placeholder', 'Ex.: Doe')
        add_attr(self.fields['password'], 'placeholder', 'Type your password here')

    password = forms.CharField(
        required=True,
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=("""
        Password must have at least one uppercase letter,
        one lowercase letter and one number. The length should be
        at last 8 characters.
        """)
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        error_messages={
            'required': 'This field is required'
        }
    )

    username = forms.CharField(
        required=True,
        error_messages={
            'required': 'This field is required'
        },
        help_text='Mandatory. 150 characters or less.\
        Letters, numbers and @/./+/-/_ only.'
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
