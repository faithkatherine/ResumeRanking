from django.urls import path
from JobPosts.views import (
	create_job_view,
	detail_job_view,
	edit_job_view,
)

app_name = 'JobPosts'

urlpatterns = [
    path('create/', create_job_view, name="create"),
    path('<slug>/', detail_job_view, name="detail"),
    path('<slug>/edit/', edit_job_view, name="edit"),
 ]