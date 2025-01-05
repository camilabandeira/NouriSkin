from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'sku', 'category', 
            'image', 'concern', 'skin_types', 'key_ingredients', 'how_to_use'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'how_to_use': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'concern': forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkbox'}),
            'skin_types': forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkbox'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'key_ingredients': forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkbox'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
