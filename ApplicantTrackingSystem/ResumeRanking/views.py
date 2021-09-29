from django.shortcuts import render
from django.http import HttpResponse
from ResumeRanking.resume_ranking import resume_ranking

# Create your views here.
 
def ranking_view(request):
    my_class = resume_ranking()
    my_class.resumeranker()

    html = "<html><body>The ranked resumes %s.</body></html>"%my_class.resumeranker()
    return HttpResponse(html)

