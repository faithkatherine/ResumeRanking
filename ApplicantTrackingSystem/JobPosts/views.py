from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

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