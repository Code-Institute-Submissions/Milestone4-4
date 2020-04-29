from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Due to extending the UserRegistrationForm password validation needs to be
# reinstated on the form.
from django.contrib.auth import password_validation
from django.core.validators import ValidationError


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter First Name'
        })
    )
    last_name = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Last Name'
        })
    )
    username = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })
    )
    email = forms.EmailField(
        required=True,
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        })
    )
    password1 = forms.CharField(
        required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )
    password2 = forms.CharField(
        required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-Enter Password'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already coupled to an "
                                  "account.")
        return email

    """Disable help text of UserCreationForm (answer got from: 
    'https://stackoverflow.com/questions/13202845/removing-help-text-from-django-usercreateform'
    & set default autofocus to first_name instead of the default field of 
    username. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['username'].widget.attrs['autofocus'] = False


class UserLogin(forms.Form):
    username = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username',
            'autofocus': 'True'
        })
    )
    password = forms.CharField(
        required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )
