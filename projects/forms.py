from django.forms import ModelForm

from projects.models import Project

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['project_name', 'deployment_date', 'is_closed']