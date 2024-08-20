from django import forms
from admin_panel.models import *
from .models import*
from django.utils import timezone

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'stock', 'color', 'available',
            'image', 'tags', 'brand_id', 'type_id', 'connection_id',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_id': forms.Select(attrs={'class': 'form-control'}),
            'type_id': forms.Select(attrs={'class': 'form-control'}),
            'connection_id': forms.Select(attrs={'class': 'form-control'}),

        }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['brand_id'].queryset = Brand.objects.filter(is_active=True)
        self.fields['type_id'].queryset = Type.objects.filter(is_active=True)
        self.fields['connection_id'].queryset = Connection_type.objects.filter(is_active=True)
        


