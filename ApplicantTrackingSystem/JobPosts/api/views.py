from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from django.contrib.auth.models import User
from JobPosts.models import JobPost
from JobPosts.api.serializers import JobPostSerializer, JobPostUpdateSerializer, JobPostCreateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/blog/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((AllowAny, ))
def api_detail_job_view(request, slug):

	try:
		job_post = JobPost.objects.get(slug=slug)
	except JobPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = JobPostSerializer(job_post)
		return Response(serializer.data)


#Response: https://127.0.0.1:8000/morfie/669689f7d7012b96e2bf26bd7d3af93b91bc4573
#Url: http://localhost/api/blog/<slug>/update
#Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_job_view(request, slug):

	try:
		job_post = JobPost.objects.get(slug=slug)
	except JobPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if job_post.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = BlogPostUpdateSerializer(job_post, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = job_post.pk
			data['title'] = job_post.title
			data['body'] = job_post.body
			data['slug'] = job_post.slug
			data['date_updated'] = job_post.date_updated
			image_url = str(request.build_absolute_uri(job_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = job_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_jobpost(request, slug):
	try:
		job_post = JobPost.objects.get(slug=slug)
	except JobPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if job_post.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/blog/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_job_view(request, slug):

	try:
		job_post = JobPost.objects.get(slug=slug)
	except JobPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if job_post.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = job_post.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_create_job_view(request):

	if request.method == 'POST':

		data = request.data
		data['author'] = request.user.pk
		serializer = JobPostCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			job_post = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = job_post.pk
			data['title'] = job_post.title
			data['body'] = job_post.body
			data['slug'] = job_post.slug
			data['date_updated'] = job_post.date_updated
			image_url = str(request.build_absolute_uri(job_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = job_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/blog/list
#		2) pagination: http://<your-domain>/api/blog/list?page=2
#		3) search: http://<your-domain>/api/blog/list?search=mitch
#		4) ordering: http://<your-domain>/api/blog/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/blog/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiJobListView(ListAPIView):
	queryset = JobPost.objects.all()
	serializer_class = JobPostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'body', 'author__username')