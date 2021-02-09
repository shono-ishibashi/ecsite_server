from django import forms

from api.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email", "password",
                  "zipcode", "address", "telephone")
