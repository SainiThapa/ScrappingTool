import uuid
from django.db import models

# Create your models here.

class Webportal(models.Model):
    page_title=models.CharField(max_length=128)
    page_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page_url=models.URLField(max_length=200)

    def __str__(self):
        return self.page_title
    

class Newsheadline(models.Model):
    news_source=models.ForeignKey(Webportal, on_delete=models.CASCADE)
    news_id=models.UUIDField(default=uuid.uuid4)
    news_title=models.CharField(max_length=512)
    news_upload_date=models.TextField()

    def __str__(self):
        return f"{self.news_title} - {self.news_source.page_title}"