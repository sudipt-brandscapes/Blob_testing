# app1/utils.py
from django.conf import settings
from azure.storage.blob import BlobServiceClient
import uuid

def upload_to_azure_blob(file, container_name=None):
    try:
        # Create blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=settings.AZURE_ACCOUNT_KEY
        )
        
        container_name = container_name or settings.AZURE_CONTAINER
        container_client = blob_service_client.get_container_client(container_name)
        
        # Generate unique filename
        file_extension = file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Upload file
        blob_client = container_client.get_blob_client(unique_filename)
        blob_client.upload_blob(file.read())
        
        # Generate URL
        blob_url = f"https://{settings.AZURE_CUSTOM_DOMAIN}/{container_name}/{unique_filename}"
        
        return {
            'url': blob_url,
            'filename': unique_filename,
            'original_name': file.name,
            'size': file.size
        }
    except Exception as e:
        print(f"Azure Blob Storage Upload Error: {e}")
        return None