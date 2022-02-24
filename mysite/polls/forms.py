from django import forms 
  
class ImagefieldForm(forms.Form): 
    name = forms.CharField() 
    description = forms.CharField()
    image = forms.ImageField()