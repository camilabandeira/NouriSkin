from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    class Meta:
        model = Profile
        fields = [
            'default_phone_number', 'default_country', 'default_postcode',
            'default_town_or_city', 'default_street_address1',
            'default_street_address2', 'default_county'
        ]
        widgets = {
            'default_phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'default_country': forms.Select(attrs={'placeholder': 'Country'}),
            'default_postcode': forms.TextInput(attrs={'placeholder': 'Postcode'}),
            'default_town_or_city': forms.TextInput(attrs={'placeholder': 'Town or City'}),
            'default_street_address1': forms.TextInput(attrs={'placeholder': 'Street Address 1'}),
            'default_street_address2': forms.TextInput(attrs={'placeholder': 'Street Address 2'}),
            'default_county': forms.TextInput(attrs={'placeholder': 'County'}),
        }

class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    email = forms.EmailField(max_length=254, required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Enter your username',
            'email': 'Enter your email',
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders.get(field_name, f"Enter {field_name}")

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
