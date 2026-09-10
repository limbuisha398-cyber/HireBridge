from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserPhone


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False
    )

    address = forms.CharField(
        max_length=255,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            profile = UserProfile.objects.create(
                user=user,
                address=self.cleaned_data.get('address', '')
            )

            phone_number = self.cleaned_data.get('phone_number')

            if phone_number:
                UserPhone.objects.create(
                    user_profile=profile,
                    phone_number=phone_number
                )

        return user

