from django import forms

from JobPosts.models import JobPost 


class CreateJobPostForm(forms.ModelForm):

	class Meta:
		model = JobPost
		fields = ['title', 'body', 'image']


class UpdateJobPostForm(forms.ModelForm):

	class Meta:
		model = JobPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		job_post = self.instance
		job_post.title = self.cleaned_data['title']
		job_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			job_post.image = self.cleaned_data['image']

		if commit:
			job_post.save()
		return job_post