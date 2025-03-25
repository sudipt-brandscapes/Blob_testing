from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Add any file validation here (size, type, etc.)
            max_size = 10 * 1024 * 1024  # 10MB example
            if file.size > max_size:
                raise forms.ValidationError(f'File size must be under {max_size//(1024*1024)}MB')
        return file