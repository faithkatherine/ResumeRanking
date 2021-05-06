from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
#from Account.models import Account



'''
# Create your models here.
categories = [
    ('1', 'Tech'),
    ('2', 'Business'),
]'''

def upload_location(instance,filename, **kwargs):
    filepath = 'Jobs/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author_id),
        title = str(instance.title),
        filename = filename
        )
    return filepath

class JobPost(models.Model):
    title           = models.CharField(null=False , max_length=50, blank=False)
    body            = models.TextField(null=False, max_length=50000, blank=False) 
    image           = models.ImageField(null=False, blank=False, upload_to = upload_location)
    #choices         =models.CharField(max_length=20, choices=categories)
    date_published  = models.DateTimeField(auto_now_add= True, verbose_name='Date Published' )
    date_updated    = models.DateTimeField(auto_now=True, verbose_name='Date Updated')
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name='job_post', verbose_name='user')
    slug            = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

@receiver (post_delete, sender=JobPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    
def pre_save_job_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_job_post_receiver, sender=JobPost)