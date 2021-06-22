from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from ResumePost.models import ResumePost
from ResumePost.api.serializers import ResumePostSerializer, ResumePostCreateSerializer


SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/blog/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated ))
def api_detail_resume_view(request, slug):

	try:
		resume_post = ResumePost.objects.get(slug=slug)
	except ResumePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = ResumePostSerializer(resume_post)
		return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_create_resume_view(request):
 
	if request.method == 'POST':

		data = request.data
		serializer = ResumePostCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			resume_post = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = resume_post.pk
			data['Applicant_name'] = resume_post.Applicant_name
			data['document'] = resume_post.document
			data['jobpost_title'] = resume_post.jobpost_title
			data['author'] = resume_post.author
			data['slug'] = resume_post.slug

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
class ApiResumeListView(ListAPIView):
	queryset = ResumePost.objects.all()
	serializer_class = ResumePostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,IsAuthenticated)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'body', 'author__username')