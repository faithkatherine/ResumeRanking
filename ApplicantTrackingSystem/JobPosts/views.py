from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse 
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

JOB_POSTS_PER_PAGE = 10

from JobPosts.models import JobPost
from JobPosts.forms import CreateJobPostForm, UpdateJobPostForm
from Account.models import Account


def create_job_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated: 
		return redirect('must_authenticate')

	form = CreateJobPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateJobPostForm()

	context['form'] = form

	return render(request, "../Templates/create_job.html", context)


def detail_job_view(request, slug):

	context = {}

	job_post = get_object_or_404(JobPost, slug=slug)
	context['job_post'] = job_post

	return render(request, '../Templates/detail_job.html', context)

def jobpost_view(request):

	context = {}

	#jobposts = JobPost.objects.all()
	#context['jobposts'] = jobposts

	#return render(request, '../Templates/job_post_snippet.html', context)

	# Search
	query = "" 
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	job_posts = sorted(get_job_queryset(query), key=attrgetter('date_updated'), reverse=True)
	


	# Pagination
	page = request.GET.get('page', 1)
	job_posts_paginator = Paginator(job_posts, JOB_POSTS_PER_PAGE)
	try:
		job_posts = job_posts_paginator.page(page)
	except PageNotAnInteger:
		job_posts = job_posts_paginator.page(JOB_POSTS_PER_PAGE)
	except EmptyPage:
		job_posts = job_posts_paginator.page(job_posts_paginator.num_pages)

	context['job_posts'] = job_posts

	return render(request, "../Templates/home.html", context)




def edit_job_view(request, slug):

	context = {} 

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	job_post = get_object_or_404(JobPost, slug=slug)

	if job_post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateJobPostForm(request.POST or None, request.FILES or None, instance=job_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			job_post = obj

	form = UpdateJobPostForm(
			initial = {
					"title": job_post.title,
					"body": job_post.body,
					"image": job_post.image,
			}
		)

	context['form'] = form
	return render(request, '../Templates/edit_job.html', context)


def get_job_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = JobPost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	