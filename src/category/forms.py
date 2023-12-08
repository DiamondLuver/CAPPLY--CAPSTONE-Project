from django import forms
from .models import Scholarship
from django.contrib.auth.models import User

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['level', 'school', 'deadline', 'more_info', 'description', 'link_web', 'country']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'more_info': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EditScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['level', 'school', 'deadline','more_info','description','link_web','country']


from .models import Comment, Reply
from django import forms

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control comment-content'}))
    class Meta:
        model = Comment
        fields = ['content']
        
class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control reply-content'}))
    class Meta:
        model = Reply
        fields = ['content']
        