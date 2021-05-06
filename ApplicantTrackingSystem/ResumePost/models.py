from django.db import models

# Create your models here.
class ResumePost(models.Model):
    Applicant_name  = models.CharField(max_length=255, blank=True)
    document        = models.FileField(upload_to='documents/')
    uploaded_at     = models.DateTimeField(auto_now_add=True)