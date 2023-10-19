from django import forms

class CustomTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'form-control'
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    content = forms.CharField(widget=CustomTextarea(attrs={'rows': 4, 'cols': 80, 'placeholder': 'Enter your message here', 'name': name}))
