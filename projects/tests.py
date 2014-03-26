from django.test import TestCase
from datetime import datetime
from projects.models import Project

class ProjectModelTests(TestCase):

	"""
	Tests that the default deployment_date of a new project is one month from today
	"""
	def test_default_date(self):
		project = Project()
		month_now = datetime.now().date().month
		next_month = month_now + 1 if month_now < 12 else 1
		self.assertEqual(project.deployment_date.month, next_month)

	"""
	Tests that the default deployment_time of a new project is 12pm
	"""
	def test_default_time(self):
		project = Project()
		self.assertEqual(project.deployment_time.hour, 12)