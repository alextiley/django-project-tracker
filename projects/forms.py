from django import forms
from django.forms import extras

from projects.models import Project

class ProjectForm(forms.ModelForm):

	project_name = forms.CharField()
	deployment_date = forms.DateTimeField(widget = extras.SelectDateWidget)
	is_closed = forms.BooleanField(required = False, label = 'Project Closed?', initial = False)

	class Meta:
		model = Project
		initial = {'is_closed': False}