from django import forms
from ResumePost.models import ResumePost

class DocumentForm(forms.ModelForm):
    class Meta:
        model = ResumePost
        fields = ('Applicant_name', 'document', )