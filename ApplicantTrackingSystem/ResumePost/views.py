from django.shortcuts import render
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

# Create your views here.
from JobPosts.models import JobPost
from ResumePost.models import ResumePost
from ResumePost. forms import CreateResumePostForm



def create_resume_view(request):
    context = {}
    if request.method == 'POST':
        form = CreateResumePostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            jobpost_title = JobPost.objects.select_related().filter(title = JobPost.title  )
            obj.jobpost_title = jobpost_title
            obj.save() 
            #Applicant_name = request.POST['name']
            #document = request.POST['myfile']
           
            form = CreateResumePostForm()
            context['form'] = form
    else:
        messages.error(request,"something is wrong")

    

    return render(request, "../Templates/resume_post.html", context)