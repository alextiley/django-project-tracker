from django import forms
from django.forms import extras

from projects.models import Project

class ProjectForm(forms.ModelForm):

	name = forms.CharField()
	deployment_date = forms.DateField(widget = extras.SelectDateWidget)
	deployment_time = forms.TimeField(help_text = 'hh:mm', initial = Project.default_time)
	is_complete = forms.BooleanField(required = False, label = 'Project Closed?', initial = False)

	class Meta:
		model = Project
		initial = {'is_complete': False}