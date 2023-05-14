from django import forms
from utils.django_forms import add_attr


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Type your username')
        add_attr(self.fields['password'], 'placeholder', 'Type your password')

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )
