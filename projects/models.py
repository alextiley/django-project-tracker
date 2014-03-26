from django.db import models

from datetime import datetime

class Project(models.Model):

	# Set default project date to the 1st of the next calendar month
	def default_date():
		date_now = datetime.now().date()
		month_now = date_now.month
		next_month = month_now + 1 if month_now < 12 else 1
		return date_now.replace(day=1, month=next_month)

	# Default time is set to 12pm
	def default_time():
		return datetime.now().time().replace(hour=12, minute=00, second=0, microsecond=0)

	def __unicode__(self):
		return str(self.id) + ": " + self.name

	name = models.CharField(max_length = 120, unique = True)
	deployment_date = models.DateField(default = default_date)
	deployment_time = models.TimeField(default = default_time)
	is_complete = models.BooleanField(default = False)