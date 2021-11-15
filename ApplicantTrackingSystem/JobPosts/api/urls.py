from django.urls import path
from JobPosts.api.views import(
	api_detail_job_view,
	api_update_job_view,
	api_delete_job_view,
	api_create_job_view,
	api_is_author_of_jobpost,
	ApiJobListView,  

)

app_name = 'JobPosts'

urlpatterns = [
	path('<slug>', api_detail_job_view, name="detail"),
	path('<slug>/update', api_update_job_view, name="update"),
	path('<slug>/delete', api_delete_job_view, name="delete"),
	path('create/', api_create_job_view, name="create"),
	path('list/', ApiJobListView.as_view(), name="list"),
	path('<slug>/is_author', api_is_author_of_jobpost, name="is_author"),

]