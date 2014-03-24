import time
from django.db import models

class Project(models.Model):

	project_name = models.CharField(max_length = 120, unique = True)
	deployment_date = models.DateTimeField()
	is_closed = models.BooleanField(default = False)

	#input_formats=['%Y-%m-%d']

	def __unicode__(self):
		return str(self.id) + ": " + self.project_name