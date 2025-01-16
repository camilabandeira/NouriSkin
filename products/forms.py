from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'sku', 'category',
            'image', 'concern', 'skin_types', 'key_ingredients', 'how_to_use',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control'
            }),
            'how_to_use': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control'
            }),
            'concern': forms.CheckboxSelectMultiple(attrs={
                'class': 'scrollable-checkbox'
            }),
            'skin_types': forms.CheckboxSelectMultiple(attrs={
                'class': 'scrollable-checkbox'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'key_ingredients': forms.CheckboxSelectMultiple(attrs={
                'class': 'scrollable-checkbox'
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        error_message = "This field is required."

        for field_name in [
            'name', 'description', 'price', 'sku', 'category',
            'image', 'how_to_use'
        ]:
            value = cleaned_data.get(field_name)
            if value in [None, '']:
                self.add_error(field_name, error_message)

        for field_name in ['concern', 'skin_types', 'key_ingredients']:
            value = cleaned_data.get(field_name)
            if not value:
                self.add_error(field_name, error_message)

        return cleaned_data
