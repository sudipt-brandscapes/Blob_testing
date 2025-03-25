from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # File size validation
            max_size = 10 * 1024 * 1024  # 10MB
            if file.size > max_size:
                raise forms.ValidationError(f'File size must be under {max_size//(1024*1024)}MB')
            
            # File type validation
            valid_extensions = ['.pdf', '.doc', '.docx', '.txt']
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError('Unsupported file extension. Please upload PDF, DOC, DOCX, or TXT files.')
                
        return file