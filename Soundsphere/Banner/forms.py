from django import forms
from admin_panel.models import *


class bannerform(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['product_id','image','name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_id': forms.Select(attrs={'class': 'form-control'}), 
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }