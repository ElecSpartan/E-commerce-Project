from django import forms

from .models import Item


iNPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model =Item
        fields = ('category', 'name', 'description', 'price' , 'image')

        widgets = {
            'category' : forms.Select(attrs={
            'class' : iNPUT_CLASSES
        }),
            'name' : forms.TextInput(attrs={
            'class' : iNPUT_CLASSES
        }),
            'description' : forms.Textarea(attrs={
            'class' : iNPUT_CLASSES
        }),        
            'price' : forms.TextInput(attrs={
            'class' : iNPUT_CLASSES
        }),   
            'image' : forms.FileInput(attrs={
            'class' : iNPUT_CLASSES
        }),              
        }