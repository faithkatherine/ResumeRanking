from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from JobPosts.models import JobPost
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.

def upload_location(instance,filename, **kwargs):
    filepath = 'Resumes/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author_id),
        title = str(instance.jobpost_title),
        filename = filename
        )
    return filepath
class ResumePost(models.Model):
    Applicant_name  = models.CharField(max_length=255, blank=False)
    document        = models.FileField(upload_to=upload_location)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    jobpost_title   = models.ForeignKey(JobPost,on_delete= models.CASCADE,related_name='resume_title',  verbose_name='title')
    author          = models.ForeignKey(JobPost,on_delete= models.CASCADE,related_name='resume_author', verbose_name='job_author')
    slug            = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.Applicant_name
    
    def get_author(self):
        return self.JobPost.author

@receiver (post_delete, sender=JobPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    
def pre_save_resume_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.Applicant_name + "-" + instance.jobpost_title.title)

pre_save.connect(pre_save_resume_post_receiver, sender=ResumePost)