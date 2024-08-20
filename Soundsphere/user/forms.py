from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=6, label='Enter OTP')


class forgotpassword(forms.Form):
    email = forms.EmailField(required=True)


class resetpassword(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=True,
        min_length=8,  # Ensure at least 8 characters
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        label="Confirm Password"
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        # Regex to enforce at least one uppercase letter, one lowercase letter, one number, and one special character
        password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

        if not password_pattern.match(new_password):
            raise forms.ValidationError(
                'Password must be at least 8 characters long, and include at least one uppercase letter, one lowercase letter, one number, and one special character.'
            )

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data