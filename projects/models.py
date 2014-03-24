from django.db import models

class Project(models.Model):

	name = models.CharField(max_length = 120, unique = True)
	deployment_date = models.DateTimeField()
	is_complete = models.BooleanField(default = False)

	def __unicode__(self):
		return str(self.id) + ": " + self.name