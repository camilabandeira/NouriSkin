from django import forms
from .models import ProductReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['title', 'name', 'email', 'rating', 'review_text', 'skin_type', 'age_group']
        widgets = {
            'skin_type': forms.RadioSelect(choices=[
                ('Normal', 'Normal'),
                ('Combination', 'Combination'),
                ('Oily', 'Oily'),
                ('Dry', 'Dry'),
            ]),
            'age_group': forms.RadioSelect(choices=[
                ('25-34', '25-34'),
                ('35-44', '35-44'),
                ('45-54', '45-54'),
                ('55+', '55+'),
            ]),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating or rating == 0:
            raise forms.ValidationError("Please select a star rating before submitting!")
        return rating
