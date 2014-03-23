from django.db import models
from django.forms import ModelForm

class Project(models.Model):

	project_name = models.CharField(max_length=120, unique=True)
	deployment_date = models.DateTimeField()
	is_closed = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.id) + ": " + self.project_name

# import time
# project.deployment_date = time.strptime("01 May 14 18:30", "%d %b %y %H:%M")

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['project_name', 'deployment_date', 'is_closed']