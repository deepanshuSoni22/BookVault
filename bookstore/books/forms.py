# books/forms.py
from django import forms
from .models import Book, AccessRequest

class BookUploadForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
                              help_text="This password will be used to encrypt the PDF")
    
    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'cover_image', 'pdf_file')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AccessRequestForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ('book',)

class AccessResponseForm(forms.ModelForm):
    class Meta:
        model = AccessRequest
        fields = ('status', 'pdf_password')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'pdf_password': forms.TextInput(attrs={'class': 'form-control'}),
        }