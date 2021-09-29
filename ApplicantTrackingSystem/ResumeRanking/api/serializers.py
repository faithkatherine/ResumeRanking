from rest_framework import serializers
from ResumeRanking.resume_ranking import resume_ranking

class ResumeRankingSerializer(serializers.ModelSerializer):
    class Meta:
    
        fields = ['pk', 'Applicant_name', 'document', 'uploaded_at', 'jobpost_title']