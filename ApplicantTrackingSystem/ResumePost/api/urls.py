from django.urls import path
from ResumePost.api.views import (
    api_detail_resume_view,
    api_create_resume_view,
)


app_name = 'ResumePost'

urlpatterns = [
    path('<slug>', api_detail_resume_view, name='details'),
    path('create/', api_create_resume_view, name='create'),
]
