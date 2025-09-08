from django import forms
from .models import Application, Job

class JobSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label="Keyword", widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(required=False, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
