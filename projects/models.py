from django.db import models
from datetime import datetime

class Project(models.Model):

	@staticmethod
	def default_time():
		return datetime.now().replace(hour=12, minute=00, second=0, microsecond=0)

	def __unicode__(self):
		return str(self.id) + ": " + self.name

	name = models.CharField(max_length = 120, unique = True)
	deployment_date = models.DateField()
	deployment_time = models.TimeField(default = default_time)
	is_complete = models.BooleanField(default = False)