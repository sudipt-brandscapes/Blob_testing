from django.db import models
from django.utils import timezone

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # This path is relative to your Azure container
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    # Add these methods for better file handling
    def get_file_name(self):
        return os.path.basename(self.file.name)
    
    def get_file_size(self):
        return self.file.size