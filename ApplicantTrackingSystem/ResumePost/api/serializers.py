from JobPosts.models import JobPost
from rest_framework import serializers
from ResumePost.models import ResumePost 

import os
from django.conf import Settings, settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage


	
class ResumePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumePost
        fields = ['pk', 'Applicant_name', 'document', 'uploaded_at', 'jobpost_title']


class ResumePostCreateSerializer(serializers.ModelSerializer):
    jobpost_title = serializers.SlugRelatedField(
    many=False,
    slug_field='title',
    queryset = JobPost.objects.all()
)

    author = serializers.SlugRelatedField(
    many=False,
    slug_field='author',
    queryset = JobPost.objects.all()
)
    class Meta:
        model = ResumePost
        fields = ['Applicant_name', 'document', 'jobpost_title', 'author', 'uploaded_at']


    def save(self):
        
        try:
            Applicant_name  = self.validated_data ['Applicant_name']
            document    = self.validated_data['document']
            
            
            resume_post = ResumePost(
                                Applicant_name  = Applicant_name,
                                document=document,
                                jobpost_title = self.validated_data['jobpost_title'],
                                author=self.validated_data['author'],
                                )

            resume_post.save()
            return resume_post
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})